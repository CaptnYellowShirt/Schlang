

#include <stdio.h>
#include <pthread.h>
#include <comedilib.h>


/* tubeStatus Flags */
#define TUBE_INPLACE    0x01    /* Tube has been created */
#define TUBE_ACTIVE     0x02    /* Tube has passed data */
#define TUBE_WAIT       0x04    /* Tube is waiting for data to appear at mouth or has been paused */

/* tubeCmd Flags */
#define TUBE_PAUSE      0x01    /* Temporarly stop data transfer */
#define TUBE_WARP       0X02    /* Increase transfer speed. e.g. stop updatting state */
#define TUBE_STOP       0x04    /* Stop data transfer, clean up tube, and remove it */



typedef struct _tubeID{

    /* User must supply the following three items: */

    comedi_t *dev;  /* Pointer to an open COMEDI device structure */
    int subdev;     /* COMEDI device subdevice number */
    FILE *dest;     /* Pointer to an open file */


    /* Code will fill-in the following items: */

    int mouth; /* File Number of location of data to be moved */
    int tail; /* File Number of the location to which the data is moved */

    pthread_t threadNo; /* Thread Number of thread preforming the data copying */

    double bytesMoved; /* Best guess at number of bytes that have been pushed though the tube */

    unsigned int tubeStatus; /* Bitwise tube status flags */
    unsigned int tubeCmd;    /* Bitwise tube command flags */



} tubeID;

typedef struct _rohrStation{
    int fd; /* File Descriptor of underlying File */

    long unsigned stationSize; /* Number of bytes of COMEDI buffer or file size */

    void *address; /* memory map address */

    long unsigned tobeSent;
    long unsigned lastSent;

    unsigned int packageSize;

} rohrStation;




int laytube_toFile(tubeID *Tube);
void *_laytube_toFile(void *args);
long unsigned _file_size(int fd);
int _growStation(rohrStation *smallStation, int expansion);
