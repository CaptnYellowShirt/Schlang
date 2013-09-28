# -*- coding: utf-8 -*-
"""
Schlangenaufbewahrungsbehälter - v0.1

aka: Schlang - A Deliberately Non-Object-Oriented Python Interface to COMEDI

COMEDI datatypes and functions are replicated though this interface using
the Python ctypes library. This allows the user to interface directly with
comedi-lib though the comfortable interface of a Python interpreter.
Object-Orientation of the interface is deliberately not provided so the coding
style will loosely mimic C -- in this way, Schlang can be used to prototype and
debug complex programs that will later be written in C.

Copyright 2013, Brandon J. Dillon <bdillon@vt.edu>
    Many Commented Sections (C) David A. Schleef
"""

from schlang import *
from math import *

subdev = c_uint(0)
chan = c_uint(0)
range = c_uint(0)
aref = c_uint(AREF_GROUND)
filename = "/dev/comedi0"

def main():
    device = pointer(comedi_t())
    data = lsampl_t()
    physical_value = c_double()
    retval = c_int()
    range_info = pointer(comedi_range())
    maxdata = lsampl_t()
    
    device = comedi_open(filename)
    if (bool(device) == False):
        comedi_perror(filename)
        return -1
    
    retval = comedi_data_read(device, subdev, chan, range, aref, byref(data))
    if (retval < 0):
        comedi_perror(filename)
        return -1
    
    comedi_set_global_oor_behavior(COMEDI_OOR_NAN)
    range_info = comedi_get_range(device, subdev, chan, range)
    maxdata = comedi_get_maxdata(device, subdev, chan)
    print("[0,%d] -> [%g,%g]\n" % (maxdata, range_info.contents.min, range_info.contents.max))
    physical_value = comedi_to_phys(data, range_info, maxdata)
    if (isnan(physical_value)):
        printf("Out of range [%g,%g]" % (range_info.contents.min, range_info.contents.max))
    else:
        printf("%g" % (physical_value))
        if (range_info.contents.unit == UNIT_volt):
            printf(" V")
        elif (range_info.contents.unit == UNIT_mA):
            printf(" mA")
        elif (range_info.contents.unit == UNIT_none):
            pass
        else:
            printf(" (unknown unit %d)" % (range_info.contents.uint))
        
        printf(" (%lu in raw units)\n" % (0xFFFFFFFF & data.value))
    
    return 0
    
# Python specific code to run main() when loaded...
if __name__ == "__main__":
    main()