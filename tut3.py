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
from os import * # <-- for read()

device = pointer(comedi_t())

class parsed_options(Structure):
    _fields_ = [("filename", c_char_p),
                ("value", c_double),
                ("subdevice", c_int),
                ("channel", c_int),
                ("aref", c_int),
                ("range", c_int),
                ("verbose", c_int),
                ("n_chan", c_int),
                ("c_scan", c_int),
                ("freq", c_double)]

BUFSZ = 10000
buf = (c_char * BUFSZ)()

N_CHANS = 256
chanlist = (c_uint * N_CHANS)()
range_info = ( POINTER( comedi_range ) * N_CHANS)()
maxdata = (lsampl_t * N_CHANS)()

def prepare_cmd_lib(dev, subdevice, n_scan, n_chan, scan_period_nanosec, cmd):
    ret = comedi_get_cmd_generic_timed(dev, subdevice, cmd, n_chan, scan_period_nanosec)
    if (ret < 0):
        printf("comedi_get_cmd_generic_timed failed\n")
        return ret
    
    cmd.contents.chanlist = cast(chanlist, POINTER(c_uint))
    cmd.contents.chanlist_len = n_chan
    if (cmd.contents.stop_src == TRIG_COUNT):
        cmd.contents.stop_arg = c_uint(n_scan.value)
        
    return 0
        
def do_cmd(dev, cmd):
    pass

def print_datum(raw, channel_index):
    physical_value = comedi_to_phys(raw, range_info[channel_index], maxdata[channel_index])
    printf("%#8.6g " % physical_value)


cmdtest_messages = ["sucess",
     "invalid source",
     "source conflict",
     "invalid argument",
     "argument conflict",
     "invalid chanlist"]


def main():
    dev = pointer(comedi_t())
    c = comedi_cmd()
    cmd = pointer(c)
    ret = c_int()
    total = 0
    i = c_int()
    subdev_flags = c_int()
    raw = lsampl_t()
    
    options = parsed_options()
    
    options.filename = c_char_p("/dev/comedi0")
    options.subdevice = c_int(0)
    options.channel = c_int(0)
    options.range = c_int(0)
    options.aref = c_int(AREF_GROUND)
    options.n_chan = c_int(2)
    options.n_scan = c_int(10000)
    options.freq = c_double(1000.0)
    
    dev = comedi_open(options.filename)
    if (not bool(dev)):
        comedi_perror(options.filename) # <-- tries to write to stdin?
        exit(1)
    
    comedi_set_global_oor_behavior(COMEDI_OOR_NUMBER)
    
    for i in range(options.n_chan):
        chanlist[i] = CR_PACK(options.channel + i, options.range, options.aref)
        range_info[i] = comedi_get_range(dev, options.subdevice, options.channel, options.range)
        maxdata[i] = comedi_get_maxdata(dev, options.subdevice, options.channel)

    prepare_cmd_lib(dev, options.subdevice, options.n_scan, options.n_chan, c_uint( int( 1e9 / options.freq) ), cmd)
    
    ret = comedi_command_test(dev, cmd)
    if (ret < 0):
        comedi_perror("comedi_command_test")
        exit(1)

    ret = comedi_command_test(dev, cmd)
    if (ret < 0):
        comedi_perror("comedi_command_test")
        exit(1)
    printf("second test returned %d (%s)\n" % (ret, cmdtest_messages[ret]) )
    if (ret != 0):    
        printf("Error preparing command\n")
        exit(1)

    ret = comedi_command(dev, cmd)
    if (ret < 0):
        comedi_perror("comedi_command")
        exit(1)
    
    subdev_flags = comedi_get_subdevice_flags(dev, options.subdevice)
    while (1):
        try:
            buf = read(comedi_fileno(dev), BUFSZ)
            ret = len(buf)
            if (ret == 0):
                break
        except:
            perror("read")
            break
        
        col = 0
        bytes_per_sample = 0
        total += len(buf)
        if (options.verbose):
            printf("read %d %d\n" % (ret, total) )
            
        if (subdev_flags & SDF_LSAMPL):
            bytes_per_sample = sizeof(lsampl_t)
        else:
            bytes_per_sample = sizeof(sampl_t)
        
        for i in range(ret / bytes_per_sample):
            if (subdev_flags & SDF_LSAMPL):
                raw = cast(buf, POINTER(lsampl_t))[i] 
            else:
                raw = cast(buf, POINTER(sampl_t))[i]
                
            print_datum(raw, col)
            col += 1
            if (col == options.n_chan):
                printf("\n")
                col = 0


# Python specific code to run main() when loaded...
if __name__ == "__main__":
    main()