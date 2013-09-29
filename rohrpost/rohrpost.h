
#include <comedilib.h>

typedef long int tubeID;


void *_laytube(void *args);
tubeID laytube_toFile(comedi_t *dev, int fileno);
