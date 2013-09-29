

#include <pthread.h>
#include <fcntl.h>
#include "rohrpost.h"



/*  laytube_toFile - Lay a new tube to a file

        #include "rohrpost.h"

        tubeID laytube_toFile(comedi_t *dev, int subdevice, int fileno)

    Description

        A fast and efficient method to asyncronously stream raw data from a COMEDI subdev ring buffer to disk.
        Function should create a child process (e.g. pneumatic tube) that is responsible for transfering data
        from the subdevice's ring buffer to the file described by fileno. Upon sucessful execution of the child
        process, function will return a valid tubeID number.
        The child process will automatically listen for data updates to the ring buffer. Once an update is detected,
        the child process will append data to the file described by fileno -- increasing the size of the file as
        data is appended.
        Child process will run until closetube() is called with the tubeID number.

    Arguments

        *dev        - Pointer to COMEDI device that is currently open
        sudevice    - Interger describing the subdevice
        fileno      - File descriptor of open, empty file

    Returns

        tubeID num  - Sucess!
        -1          - Bad device
        -2          - Bad file
*/


tubeID laytube_toFile(comedi_t *dev, int fileno){

    const char *board_name;
    int file_flags;
    pthread_t digger;
    int files[2];



    // Check COMEDI device and subdevice
    board_name = comedi_get_board_name(dev);

    if (board_name == NULL){
        return(-1);
    }


    // Check fileno
    file_flags = fcntl(fileno, F_GETFD);

    if (file_flags == -1){
        return(-2);
    }

    files[0] = comedi_fileno(dev);
    files[1] = fileno;

    pthread_create(&digger, NULL, _laytube, (void *)files );

    return((tubeID) digger);

}


void *_laytube(void *args){

    int mouth_fd = ((int *)args)[0];
    int tail_fd = ((int *)args)[1];

    printf("\n\nmouth_fd: %i\ntail_fd: %i\n\n", mouth_fd, tail_fd);

    pthread_exit(NULL);

}
