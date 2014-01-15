
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
    pTube->tail = pTube->dest;

    file_flags[1] = fcntl(pTube->tail, F_GETFD);

    // Is fd open? ...
    if (file_flags[1] == EBADF){
        return(-2);
    }

    /* Create new thread instance of data handeling process */
    pthread_create(&(pTube->threadNo), NULL, _laytube_toFile, (void *)pTube );

    /* Block laytube_toFile from returning until new pTube is setup */
    while ( !(pTube->tubeStatus & TUBE_INPLACE) || (pTube->tubeStatus & TUBE_FAILED) ){
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

    long int test;



    /* Populate Station Information */
    printf("\npopulating...\n");
    sendingStation.stationSize = comedi_get_buffer_size(pTube->dev, pTube->subdev);
    sendingStation.fd = pTube->mouth;
    receivingStation.stationSize = _file_size(pTube->tail);
    receivingStation.fd = pTube->tail;

    /* Set size of samples */
    printf("\nset size...\n");
    subdev_flags = comedi_get_subdevice_flags(pTube->dev, pTube->subdev);
    if (subdev_flags | SDF_LSAMPL){
        sendingStation.packageSize = sizeof(lsampl_t);
    }else{
        sendingStation.packageSize = sizeof(sampl_t);
    }
    receivingStation.packageSize = sendingStation.packageSize;


    /* Set up memory maps */
    sendingStation.address = mmap(NULL, sendingStation.stationSize, PROT_READ, MAP_SHARED, pTube->mouth, 0);
    if (sendingStation.address == MAP_FAILED){
        pTube->tubeStatus = pTube->tubeStatus | TUBE_FAILED;
        pthread_exit(NULL);
    }

    /* Check for empty file */
    if (receivingStation.stationSize < 1){
        /* Nothing to map! */
        receivingStation.stationSize = sysconf(_SC_PAGESIZE); /*  Let's make the file one page-size in length */
        ftruncate(receivingStation.fd, receivingStation.stationSize);
        test = sysconf(_SC_PAGESIZE);
        printf("\nsysconf: %li\n", test);
        printf("\nstationSize: %lu\n", receivingStation.stationSize);
    }

    receivingStation.address = mmap(NULL, receivingStation.stationSize, PROT_WRITE | MAP_HUGETLB, MAP_SHARED, pTube->tail, 0);
    if (receivingStation.address == MAP_FAILED){
        pTube->tubeStatus = pTube->tubeStatus | TUBE_FAILED;
        pthread_exit(NULL);
    }

    printf("\nset flags....\n");
    /* Stations are setup... set status and command flags... */
    sendingStation.lastSent = 0;
    sendingStation.tobeSent = 0;
    pTube->tubeCmd = 0x00;
    pTube->tubeStatus = TUBE_INPLACE; /* <-- un-blocks laytube_toFile to return to calling function */


    /* Core algorithm - This while loop handles the data transfer from ring buffer to disk */
    while( !(pTube->tubeCmd & TUBE_STOP )){


        sendingStation.tobeSent += comedi_get_buffer_contents(pTube->dev, pTube->subdev); /* bytes */

        printf("\ncomedi: %lu", sendingStation.tobeSent);

        /* If toBeSent is the same number as lastSent then no data is ready for pick up ... rest */
        if (sendingStation.tobeSent == sendingStation.lastSent){
            usleep(10); /* TODO: optimize by setting sleep number to best guess at when data might show up again */
            /* do other stuff like update pTube status w/ extra time */
        }
        else /* Assume fresh data is in ring buffer... */
        {
            overhead = receivingStation.stationSize - (sendingStation.lastSent + sendingStation.tobeSent);
            printf("\noverhead: %i\n", overhead);
            fflush(stdout);
            if (overhead <= 0){
                printf("\ngrowing...\n\n"); fflush(stdout);
                if (_growStation(&receivingStation, 20*sysconf(_SC_PAGESIZE))){ /* Expand by one page-size */
                    /* Error checking */
                    printf("\nGrow Error!\n");
                }
            }

            dest = receivingStation.address + sendingStation.lastSent;

            /* Mem Copy ... */
            printf("\nsendingStation.tobeSent: %lu\n", sendingStation.tobeSent);
            for (i = 0; i < sendingStation.tobeSent+1; i++ ){
                offset = (sendingStation.lastSent + i) % sendingStation.stationSize;
                *(unsigned char *)(dest + i) = *(unsigned char *)(sendingStation.address + offset ); /* optimize by using larger chunks than 'char' */
                printf("%02X ", *(unsigned char *)(sendingStation.address + offset));
            }
            printf("\n\nend mem copy...\n");
            /* Update station status */
            comedi_mark_buffer_read(pTube->dev, pTube->subdev, sendingStation.tobeSent);
            sendingStation.lastSent += sendingStation.tobeSent;

            msync(receivingStation.address, receivingStation.stationSize, 0);
            pTube->tubeCmd = TUBE_STOP;
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
    if (ftruncate(smallStation->fd, newSz) ){
        printf("\nftruncae\n");
        return -1;
    }

    /* ... and memory map */
    smallStation->address = mremap(smallStation->address, oldSz, newSz, MREMAP_MAYMOVE);
    if (smallStation->address == MAP_FAILED){
        printf("\naddress: %li\n", *(long int *)smallStation->address);
        printf("\nmremap\n");
        return -1;
    }

    smallStation->stationSize = newSz;

    return 0;
}
