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


subdev = c_uint(0)
chan = c_uint(0)
range = c_uint(0) 
aref = c_uint(AREF_GROUND);

def main():
    it = POINTER(comedi_t)
    chan = c_uint(0)        
    data = lsampl_t()
    retval = c_int()
    
    it = comedi_open("/dev/comedi0")
    
    if (it == None):
        comedi_perror("comedi_open")
        return -1
        
    
    retval = comedi_data_read(it, subdev, chan, range, aref, byref(data))
    
    if (retval < 0):
        comedi_perror("comedi_data_read")
        return -1
        
    print data.value
    
    return 0
    
# Python specific code to run main() when loaded...
if __name__ == "__main__":
    main()
        