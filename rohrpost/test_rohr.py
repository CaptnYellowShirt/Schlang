# -*- coding: utf-8 -*-


from ctypes import *
from schlang import *
import tempfile
import time


class tubeID(Structure):
    _fields_ = [("dev", POINTER(comedi_t)),
                ("subdev", c_int),
                ("dest", c_int),
                ("mouth", c_int),
                ("tail", c_int),
                ("threadNo", c_ulong),
                ("bytesMoved", c_ulong),
                ("tubeStatus", c_uint),
                ("tubeCmd", c_uint)]

class _rohrStation(Structure):
    _fields_ = [("fd", c_int),
                ("stationSize", c_ulong),
                ("address", POINTER(None)),
                ("tobeSent", c_ulong),
                ("lastSent", c_ulong),
                ("packageSize", c_uint)]

_pTube = tubeID()
pTube = pointer(_pTube)


_librohrpost = CDLL('./librohrpost.so')

_grab = _librohrpost.__getitem__


laytube_toFile = _grab("laytube_toFile")
laytube_toFile.restype = c_int
laytube_toFile.argtypes = [POINTER(tubeID)]





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


if(1):
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
    options.n_scan = c_int(100)
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


    pTube.contents.dev = dev    
    temp = tempfile.TemporaryFile(mode='w+b')
    pTube.contents.dest = temp.fileno()
    laytube_toFile(pTube)

   
    subdev_flags = comedi_get_subdevice_flags(dev, options.subdevice)

    time.sleep(3)

    pTube.contents.tubeCmd = 4
 
