
#define _GNU_SOURCE 1
#include <unistd.h>
#include <sys/mman.h>
#include <errno.h>
#include <fcntl.h>
#include <sys/stat.h>
#include "rohrpost.h"

/* Face Meltingly Fast */

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
         -3         - Other

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

    /* Create new thread instance of data copying process */
    pthread_create(&(pTube->threadNo), NULL, _laytube_toFile, (void *)pTube );

    /* Block laytube_toFile from returning until new pTube is setup or failes */
    while ( !(pTube->tubeStatus & TUBE_INPLACE) || (pTube->tubeStatus & TUBE_FAILED) ){
        usleep(100);  /* 1/10 sec */
    }

    if (pTube->tubeStatus & TUBE_FAILED){
        return(-3);
    }else{
        return(0);
    }


}


void *_laytube_toFile(void *args){

    long unsigned int expansion_size;
    void *pause_after;
    tubeID *pTube;
    rohrStation sendingStation;
    rohrStation receivingStation;

    pTube = (tubeID *) args;


    /* Populate Station Information */
    sendingStation.stationSize = comedi_get_buffer_size(pTube->dev, pTube->subdev);
    receivingStation.stationSize = _file_size(pTube->tail);
    expansion_size = 64 * sysconf(_SC_PAGESIZE); /* Set file expansion size to a mulitple of memory page size */
    if (expansion_size < sendingStation.stationSize){
        pTube->tubeStatus = pTube->tubeStatus | TUBE_FAILED;
        pthread_exit(NULL);
    }

    /* Check for empty file */
    if (receivingStation.stationSize < 1){
        receivingStation.stationSize = expansion_size; /*  Let's make the file one page-size in length */
        ftruncate(pTube->tail, receivingStation.stationSize);
    }

    /* Set up COMEDI ring buffer memory map */
    sendingStation.firstByte = mmap(NULL, sendingStation.stationSize, PROT_READ, MAP_SHARED, pTube->mouth, 0);
    if (sendingStation.firstByte == MAP_FAILED){
        pTube->tubeStatus = pTube->tubeStatus | TUBE_FAILED;
        pthread_exit(NULL);
    }
    sendingStation.address = sendingStation.firstByte;
    sendingStation.lastByte = sendingStation.firstByte + sendingStation.stationSize - 1; /* Last valid byte */

    /* Set up HDD file memory map */
    receivingStation.firstByte = mmap(NULL, receivingStation.stationSize, PROT_WRITE | MAP_HUGETLB, MAP_SHARED, pTube->tail, 0);
    if (receivingStation.firstByte == MAP_FAILED){
        pTube->tubeStatus = pTube->tubeStatus | TUBE_FAILED;
        pthread_exit(NULL);
    }
    receivingStation.address = receivingStation.firstByte;
    receivingStation.lastByte = receivingStation.firstByte + receivingStation.stationSize - 1; /* Last valid byte */


    /* Stations are setup... set status and command flags... */
    pTube->tubeCmd = 0x00;
    pTube->tubeStatus = TUBE_INPLACE; /* <-- un-blocks laytube_toFile to return to calling function */

    /* Core algorithm - This while loop handles the data transfer from ring buffer to disk */
    while( !(pTube->tubeCmd & TUBE_STOP) ){

        /* Check if the storage file is out or about to be out of space */
        if (sendingStation.stationSize >= (receivingStation.lastByte - receivingStation.address) ){
           if (_growStation(&receivingStation, pTube->tail, expansion_size) == -1){
                pTube->tubeStatus = pTube->tubeStatus | TUBE_FAILED;
                pthread_exit(NULL);
           }
        }

        pause_after = sendingStation.firstByte + comedi_get_buffer_contents(pTube->dev, pTube->subdev) - 1;

        if (pause_after < sendingStation.address){
            pTube->bytesMoved = receivingStation.address - receivingStation.firstByte;
            /* comedi_poll(pTube->dev, pTube->subdev)); */
            usleep(10); /* TODO: optimize by setting sleep number to best guess at when data might show up again */
        }
        else if (pause_after < sendingStation.lastByte) /* Confirm COMEDI ring buffer has not aliased */
        {
            do {
                *((CARRIER *)receivingStation.address++) = *((CARRIER *)sendingStation.address++);
            } while(sendingStation.address <= pause_after);
        }
        else if (pause_after >= sendingStation.lastByte) /* COMEDI ring buffer has aliased... copy up to end of ring buffer and reset */
        {
            do {
                *((CARRIER *)receivingStation.address++) = *((CARRIER *)sendingStation.address++);
            } while(sendingStation.address <= sendingStation.lastByte);

            comedi_mark_buffer_read(pTube->dev, pTube->subdev, sendingStation.stationSize); /* Reset the ring buffer mark */
            sendingStation.address = sendingStation.firstByte;
        }
        else
        {
            pTube->tubeStatus = pTube->tubeStatus | TUBE_FAILED;
            pthread_exit(0);
        }
    }

    /* Clean up Stations, truncate file, flush tube */
    expansion_size = receivingStation.address - receivingStation.firstByte; /* 'address' should point to one byte past last byte written */
    ftruncate(pTube->tail, expansion_size);
    fsync(pTube->tail);
    pTube->bytesMoved = expansion_size;

    pTube->tubeStatus = pTube->tubeStatus | TUBE_EXIT;

    pthread_exit(0);
}


long unsigned _file_size(int fd){
    struct stat buf;

    fstat(fd, &buf);

    return buf.st_size;
}


int _growStation(rohrStation *smallStation, int fd, long int expansion){

    long int oldSz = smallStation->stationSize;
    long int newSz = oldSz + expansion;
    long int offset = smallStation->address - smallStation->firstByte;

    /* Expand underlying file ... */
    if (ftruncate(fd, newSz) ){
        return -1;
    }

    /* ... and memory map */
    smallStation->firstByte = mremap(smallStation->firstByte, oldSz, newSz, MREMAP_MAYMOVE);
    if (smallStation->firstByte == MAP_FAILED){
        return -1;
    }

    smallStation->address = smallStation->firstByte + offset;
    smallStation->stationSize = newSz;
    smallStation->lastByte = newSz + smallStation->firstByte - 1;

    return 0;
}
