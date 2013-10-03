
#define _GNU_SOURCE 1
#include <unistd.h>
#include <sys/mman.h>
#include <errno.h>
#include <fcntl.h>
#include <sys/stat.h>
#include "rohrpost.h"


/*  laytube_toFile - Lay a new penumatic tube to a file

        #include "rohrpost.h"

        int laytube_toFile(tubeID *pTube)

    Description

        A fast and efficient method to asyncronously stream raw data
        from a COMEDI subdev ring buffer to disk. Function creates a
        child thread (e.g. pneumatic tube) that is responsible for
        transfering data from the subdevice's ring buffer (described
        by pTube.mouth) to a disk file (described by pTube.tail).

        The child thread will automatically listen for data updates
        to the ring buffer. Once an update is detected, the child
        thread will append data to the file described by pTube.tail
        -- increasing the size of the file as data is appended.

        File described by pTube.tail must be opened in a binary and
        append mode. File may be preallocated, however laytube_toFile
        will overwrite anything that is present in the file upon
        execution.

        Child thread will run until pTube.tubeCmd is set with the
        TUBE_STOP flag. Once this flag is detected, the child will
        stop its data transfer, perform a final update to the
        TubeID structure, truncate the pTube.tail file to a size
        which corresponds to the last data byte that was moved,
        and close the thread.

        Upon execution laytube_toFile will update the TubeID structure
        and return a integer describing its execution sucess.

    Arguments

        *pTube   - Pointer to an instance of a TubeID strucutre

    Returns

         0          - Sucess!
         -1         - Bad COMEDI File Descriptor
         -2         - Bad destiation File Descriptor

*/


int laytube_toFile(tubeID *pTube){

    int file_flags[2];


    /* Check COMEDI file descriptor */
    pTube->mouth = comedi_fileno(pTube->dev);

    file_flags[0] = fcntl(pTube->mouth, F_GETFD);

    // Is fd open? ...
    if (file_flags[0] == EBADF){
        return(-1);
    }


    // Check destition file descriptor
    pTube->tail = fileno(pTube->dest);

    file_flags[1] = fcntl(pTube->tail, F_GETFD);

    // Is fd open? ...
    if (file_flags[1] == EBADF){
        return(-2);
    }

    /* Create new thread instance of data handeling process */
    pthread_create(&(pTube->threadNo), NULL, _laytube_toFile, (void *)pTube );

    /* Block laytube_toFile from returning until new pTube is setup */
    while ( !(pTube->tubeStatus & TUBE_INPLACE)){
        usleep(100);  /* 1/10 sec */
    }

    return(0);

}


void *_laytube_toFile(void *args){

    int i;
    int subdev_flags;
    int overhead;
    tubeID *pTube;
    rohrStation sendingStation;
    rohrStation receivingStation;

    pTube = (tubeID *) args;

    void *dest;
    int offset;



    /* Populate Station Information */
    sendingStation.stationSize = comedi_get_buffer_size(pTube->dev, pTube->subdev);
    sendingStation.fd = pTube->mouth;
    receivingStation.stationSize = _file_size(pTube->tail);
    receivingStation.fd = pTube->tail;

    /* Set size of samples */
    subdev_flags = comedi_get_subdevice_flags(pTube->dev, pTube->subdev);
    if (subdev_flags | SDF_LSAMPL){
        sendingStation.packageSize = sizeof(lsampl_t);
    }else{
        sendingStation.packageSize = sizeof(sampl_t);
    }
    receivingStation.packageSize = sendingStation.packageSize;


    /* Set up memory maps */
    sendingStation.address = mmap(NULL, sendingStation.stationSize, PROT_READ, MAP_PRIVATE, pTube->mouth, 0);
    if (sendingStation.address == MAP_FAILED){
        pthread_exit(NULL);
    }

    receivingStation.address = mmap(NULL, receivingStation.stationSize, PROT_WRITE, MAP_SHARED | MAP_HUGETLB, pTube->tail, 0);
    if (receivingStation.address == MAP_FAILED){
        pthread_exit(NULL);
    }


    /* Stations are setup... set status and command flags... */
    sendingStation.lastSent = 0;
    sendingStation.tobeSent = 0;
    pTube->tubeCmd = 0x00;
    pTube->tubeStatus = TUBE_INPLACE; /* <-- un-blocks laytube_toFile to return to calling function */



    while( !(pTube->tubeCmd & TUBE_STOP )){

        sendingStation.tobeSent += comedi_get_buffer_contents(pTube->dev, pTube->subdev); /* bytes */

        /* If toBeSent is the same number as lastSent then no data is ready for pick up ... rest */
        if (sendingStation.tobeSent == sendingStation.lastSent){
            usleep(10); /* TODO: optimize by setting sleep number to best guess at when data might show up again */
            /* do other stuff like update pTube status */
        }
        else /* Assume fresh data is in ring buffer... */
        {
            overhead = receivingStation.stationSize - sendingStation.lastSent + sendingStation.tobeSent;
            if (overhead <= 0){
                if (_growStation(&receivingStation, 65536)){
                    /* Error checking */
                }
            }

            dest = receivingStation.address + sendingStation.lastSent;

            /* Mem Copy ... */
            for (i = 1; i > sendingStation.tobeSent; i++ ){
                offset = (sendingStation.lastSent + i) % sendingStation.packageSize;
                *(char *)(dest + i) = *(char *)(sendingStation.address + offset );
            }

            /* Update station status */

        }


    }

    /* clean up Stations, flush tube, truncate file */
    pthread_exit(0);


}


long unsigned _file_size(int fd){
    struct stat buf;

    fstat(fd, &buf);

    return buf.st_size;
}


int _growStation(rohrStation *smallStation, int expansion){

    int oldSz = smallStation->stationSize;
    int newSz = oldSz + expansion;


    /* Expand underlying file ... */
    if (ftruncate(smallStation->fd, expansion) ){
        return -1;
    }

    /* ... and memory map */
    if ((smallStation->address = mremap(smallStation->address, oldSz, newSz, MREMAP_MAYMOVE) )) {
        return -1;
    }

    smallStation->stationSize = newSz;

    return 0;
}
