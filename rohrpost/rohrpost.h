

#include <stdio.h>
#include <pthread.h>
#include <comedilib.h>


/* tubeStatus Flags */
#define TUBE_INPLACE    0x001     /* Tube has been created */
#define TUBE_ACTIVE     0b002     /* Tube has passed data */
#define TUBE_WAIT       0x004     /* Tube is waiting for data to appear at mouth or has been paused */
#define TUBE_FAILED     0x008     /* Tube has thrown an unrecoverable error - check for rats */
#define TUBE_EXIT       0x010     /* Tube has sucessuflly exited - congrats */

/* tubeCmd Flags */
#define TUBE_PAUSE      0x001      /* Temporarly stop data transfer */
#define TUBE_WARP       0x002      /* Increase transfer speed. e.g. stop updatting state */
#define TUBE_STOP       0x004      /* Stop data transfer, clean up tube, and remove it */

/* Pneumatic Tube "Carrier" - size of memory copy chunk */
#define CARRIER char /* <- 8bits */


typedef struct _tubeID{

    /* User must supply the following three items: */

    comedi_t *dev;  /* Pointer to an open COMEDI device structure */
    int subdev;     /* COMEDI device subdevice number */
    int dest;       /* File Descriptor for an open file */


    /* Code will fill-in the following items: */

    int mouth; /* File Number of location of data to be moved */
    int tail; /* File Number of the location to which the data is moved */

    pthread_t threadNo; /* Thread Number of thread preforming the data copying */

    long unsigned int bytesMoved; /* Best guess at number of bytes that have been pushed though the tube */

    unsigned int tubeStatus; /* Bitwise tube status flags */
    unsigned int tubeCmd;    /* Bitwise tube command flags */



} tubeID;

typedef struct _rohrStation{
    long unsigned stationSize; /* Number of bytes of COMEDI buffer or file size */
    void *firstByte; /* memory map address */
    void *lastByte;

    void *address;


} rohrStation;




int laytube_toFile(tubeID *Tube);
void *_laytube_toFile(void *args);
long unsigned _file_size(int fd);
int _growStation(rohrStation *smallStation, int fd, long int expansion);
