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


from ctypes import *


##############################################################################
#                   - Begin CONFIGURATION Section -
##############################################################################


_libcomedi = CDLL('/usr/lib/libcomedi.so.0')

# Import outdated functions?
import_deprecated = True

# Execute typedef statements?
typedef = True

# Execute COMEDI_STRICT_ABI typedef statements?
strict_abi = False

# Enforce strict ctypes types consistancy?
strict_ctypes = False



# Define a 'ctype' for plain c void type (not void pointer)
class c_void:
    def from_param(self):
        return self

# Define a 'enum' class to be inhereited by emulated types
class c_enum(c_int):    
    def __str__(self):
        return str(self.value)
    
    def __repr__(self):
        return self.__class__.__name__


# Overload ctypes primatives so that c functions are forced to accept and
# return only proper ctypes primatives and not closely associated values
# e.g. c_int not int

if (strict_ctypes):
    class c_bool(c_bool):
        pass
    class c_char(c_char):
        pass
    class c_wchar(c_wchar):
        pass
    class c_byte(c_byte):
        pass
    class c_ubyte(c_ubyte):
        pass
    class c_short(c_short):
        pass
    class c_ushort(c_ushort):
        pass
    class c_int(c_int):
        pass
    class c_uint(c_uint):
        pass
    class c_long(c_long):
        pass
    class c_ulong(c_ulong):
        pass
    class c_longlong(c_longlong):
        pass
    class c_ulonglong(c_ulonglong):
        pass
    class c_float(c_float):
        pass
    class c_double(c_double):
        pass
    class c_longdouble(c_longdouble):
        pass
    class c_char_p(c_char_p):
        pass
    class c_wchar_p(c_wchar_p):
        pass
    class c_void_p(c_void_p):
        pass




##############################################################################
#                   - Begin TYPE DEFINITION section -
##############################################################################


##############################################################################
# Preprocessor Definitions 
#

COMEDI_NAMELEN = 20                                                             #   #define COMEDI_NAMELEN 20  /* max length of device and driver names */
COMEDI_MAX_NUM_POLYNOMIAL_COEFFICIENTS = c_int(4)                               #   #define COMEDI_MAX_NUM_POLYNOMIAL_COEFFICIENTS 4")
COMEDI_POLYNOMIAL_COEFFS = COMEDI_MAX_NUM_POLYNOMIAL_COEFFICIENTS               #   that's a lot to type...

CS_MAX_AREFS_LENGTH = 4                                                         #   define CS_MAX_AREFS_LENGTH 4

UNIT_volt = 0                                                                   #   define UNIT_volt		0
UNIT_mA = 1                                                                     #   define UNIT_mA			1
UNIT_none = 2                                                                   #   define UNIT_none		2

####################
# Trigger Sources 

TRIG_ANY = 0xffffffff                                                           #   define TRIG_ANY	0xffffffff
TRIG_INVALID = 0x00000000                                                       #   define TRIG_INVALID	0x00000000

TRIG_NONE = 0x00000001                                                          #   define TRIG_NONE	0x00000001	/* never trigger */
TRIG_NOW = 0x00000002                                                           #   define TRIG_NOW	0x00000002	/* trigger now + N ns */
TRIG_FOLLOW = 0x00000004                                                        #   define TRIG_FOLLOW	0x00000004	/* trigger on next lower level trig */
TRIG_TIME = 0x00000008                                                          #   define TRIG_TIME	0x00000008	/* trigger at time N ns */
TRIG_TIMER = 0x00000010                                                         #   define TRIG_TIMER	0x00000010	/* trigger at rate N ns */
TRIG_COUNT = 0x00000020                                                         #   define TRIG_COUNT	0x00000020	/* trigger when count reaches N */
TRIG_EXT = 0x00000040                                                           #   define TRIG_EXT	0x00000040	/* trigger on external signal N */
TRIG_INT = 0x00000080                                                           #   define TRIG_INT	0x00000080	/* trigger on comedi-internal signal N */
TRIG_OTHER = 0x00000100                                                         #   define TRIG_OTHER	0x00000100	/* driver defined */

####################
# Subdevice Flags 

SDF_BUSY = 0x0001                                                               #   define SDF_BUSY	0x0001	/* device is busy */
SDF_BUSY_OWNER = 0x0002                                                         #   define SDF_BUSY_OWNER	0x0002	/* device is busy with your job */
SDF_LOCKED = 0x0004                                                             #   define SDF_LOCKED	0x0004	/* subdevice is locked */
SDF_LOCK_OWNER = 0x0008                                                         #   define SDF_LOCK_OWNER	0x0008	/* you own lock */
SDF_MAXDATA = 0x0010                                                            #   define SDF_MAXDATA	0x0010	/* maxdata depends on channel */
SDF_FLAGS = 0x0020                                                              #   define SDF_FLAGS	0x0020	/* flags depend on channel */
SDF_RANGETYPE = 0x0040                                                          #   define SDF_RANGETYPE	0x0040	/* range type depends on channel */
SDF_MODE0 = 0x0080                                                              #   define SDF_MODE0	0x0080	/* can do mode 0 */
SDF_MODE1 = 0x0100                                                              #   define SDF_MODE1	0x0100	/* can do mode 1 */
SDF_MODE2 = 0x0200                                                              #   define SDF_MODE2	0x0200	/* can do mode 2 */
SDF_MODE3 = 0x0400                                                              #   define SDF_MODE3	0x0400	/* can do mode 3 */
SDF_MODE4 = 0x0800                                                              #   define SDF_MODE4	0x0800	/* can do mode 4 */
SDF_CMD = 0x1000                                                                #   define SDF_CMD		0x1000	/* can do commands (deprecated) */
SDF_SOFT_CALIBRATED = 0x2000                                                    #   define SDF_SOFT_CALIBRATED	0x2000	/* subdevice uses software calibration */
SDF_CMD_WRITE = 0x4000                                                          #   define SDF_CMD_WRITE		0x4000	/* can do output commands */
SDF_CMD_READ = 0x8000                                                           #   define SDF_CMD_READ		0x8000	/* can do input commands */

SDF_READABLE = 0x00010000                                                       #   define SDF_READABLE	0x00010000	/* subdevice can be read (e.g. analog input) */
SDF_WRITABLE = 0x00020000                                                       #   define SDF_WRITABLE	0x00020000	/* subdevice can be written (e.g. analog output) */
SDF_WRITEABLE = SDF_WRITABLE                                                    #   define SDF_WRITEABLE	SDF_WRITABLE	/* spelling error in API */
SDF_INTERNAL = 0x00040000                                                       #   define SDF_INTERNAL	0x00040000	/* subdevice does not have externally visible lines */
SDF_RT = 0x00080000                                                             #   define SDF_RT		0x00080000	/* DEPRECATED: subdevice is RT capable */
SDF_GROUND = 0x00100000                                                         #   define SDF_GROUND	0x00100000	/* can do aref=ground */
SDF_COMMON = 0x00200000                                                         #   define SDF_COMMON	0x00200000	/* can do aref=common */
SDF_DIFF = 0x00400000                                                           #   define SDF_DIFF	0x00400000	/* can do aref=diff */
SDF_OTHER = 0x00800000                                                          #   define SDF_OTHER	0x00800000	/* can do aref=other */
SDF_DITHER = 0x01000000                                                         #   define SDF_DITHER	0x01000000	/* can do dithering */
SDF_DEGLITCH = 0x02000000                                                       #   define SDF_DEGLITCH	0x02000000	/* can do deglitching */
SDF_MMAP = 0x04000000                                                           #   define SDF_MMAP	0x04000000	/* can do mmap() */
SDF_RUNNING = 0x08000000                                                        #   define SDF_RUNNING	0x08000000	/* subdevice is acquiring data */
SDF_LSAMPL = 0x10000000                                                         #   define SDF_LSAMPL	0x10000000	/* subdevice uses 32-bit samples */
SDF_PACKED = 0x20000000                                                         #   define SDF_PACKED	0x20000000	/* subdevice can do packed DIO */
                                                                                #   /* re recyle these flags for PWM */
SDF_PWM_COUNTER = SDF_MODE0                                                     #   define SDF_PWM_COUNTER SDF_MODE0       /* PWM can automatically switch off */
SDF_PWM_HBRIDGE = SDF_MODE1                                                     #   define SDF_PWM_HBRIDGE SDF_MODE1       /* PWM is signed (H-bridge) */

####################
#   AREF_*
#
#   The aref argument indicates what reference you want the device to use. 
#   It can be any of the following:
#   
#   AREF_GROUND     is for inputs/outputs referenced to ground. 
#   AREF_COMMON     is for a “common” reference (the low inputs of all the 
#                    channels are tied together, but are isolated from ground). 
#   AREF_DIFF       is for differential inputs/outputs. 
#   AREF_OTHER      is for any reference that does not fit into the above categories. 
#
#   Particular drivers may or may not use the AREF flags. If they are not 
#   supported, they are silently ignored. 
#

AREF_GROUND = 0x00                                                             #    #define AREF_GROUND	0x00	/* analog ref = analog ground */
AREF_COMMON = 0x01                                                             #    #define AREF_COMMON	0x01	/* analog ref = analog common */
AREF_DIFF = 0x02                                                               #    #define AREF_DIFF	      0x02	/* analog ref = differential */
AREF_OTHER = 0x03                                                              #    #define AREF_OTHER	      0x03	/* analog ref = other (undefined) */
                                                                               
                                                                    
####################
#   CR_PACK
#
#   CR_PACK(chan, rng, aref) is used to initialize the elements of the chanlist
#   array in the comedi_cmd data structure, and the chanspec member of the 
#   comedi_insn structure.  The chan argument is the channel you wish to use, 
#   with the channel numbering starting at zero.  The range rng is an index, 
#   starting at zero, whose meaning is device dependent. The comedi_get_n_ranges
#   and comedi_get_range functions are useful in discovering information about
#   the available ranges.

def CR_PACK(chan, rng, aref):                                                   #   #define CR_PACK(chan,rng,aref)      ( (((aref)&0x3)<<24) | (((rng)&0xff)<<16) | (chan) )
    return  (((aref)&0x3)<<24) | (((rng)&0xff)<<16) | (chan)                  



####################
#   CR_*
#
#   CR_ALT_FILTER,  (all the same) specify that some sort of filtering is to 
#   CR_DITHER,      be done on the channel, trigger source, etc. 
#   CR_DEGLITCH    
#   
#   CR_ALT_SOURCE   specifies that some alternate source is to be used for the
#                   channel (usually a calibration source). 
#
#   CR_EDGE         is usually combined with a trigger source number to 
#                   specify that the trigger source is edge-triggered if the 
#                   hardware and driver supports both edge-triggering and 
#                   level-triggering. If both are supported, not asserting 
#                   this flag specifies level-triggering. 
#
#   CR_INVERT       specifies that the trigger source, gate source, etc. is 
#                   to be inverted. 

CR_FLAGS_MASK = 0xfc000000                                                      #   #define CR_FLAGS_MASK	0xfc000000
CR_ALT_FILTER = 1<<26                                                           #   #define CR_ALT_FILTER	(1<<26)
CR_DITHER = CR_ALT_FILTER                                                       #   #define CR_DITHER		CR_ALT_FILTER
CR_DEGLITCH = CR_ALT_FILTER                                                     #   #define CR_DEGLITCH		CR_ALT_FILTER
CR_ALT_SOURCE = 1<<27                                                           #   #define CR_ALT_SOURCE	(1<<27)
CR_EDGE = 1<<30                                                                 #   #define CR_EDGE	(1<<30)
CR_INVERT = 1<<31                                                               #   #define CR_INVERT	(1<<31)



####################
#   CR_PACK_FLAGS
#
#   CR_PACK_FLAGS(chan, range, aref, flags) is similar to CR_PACK but can be 
#   used to combine one or more flag bits (bitwise-ORed together in the flags 
#   parameter) with the other parameters.
#
#   Depending on context, the chan parameter might not be a channel; it could 
#   be a trigger source, clock source, gate source etc. (in which case, the 
#   range and aref parameters would probably be set to 0), and the flags would 
#   modify the source in some device-dependant way. 

def CR_PACK_FLAGS(chan, range, aref, flags):                                    #   #define CR_PACK_FLAGS(chan, range, aref, flags)  (CR_PACK(chan, range, aref) | ((flags) & CR_FLAGS_MASK))
    return c_int(CR_PACK(chan, range, aref) | ((flags) & CR_FLAGS_MASK))








##############################################################################
#   comedi_conversion_direction
#
#   A comedi_conversion_direction is used to choose between converting data 
#   from Comedi's integer sample values to a physical value (COMEDI_TO_PHYSICAL),
#   and converting from a physical value to Comedi's integer sample values 
#   (COMEDI_FROM_PHYSICAL). 

class comedi_conversion_direction(c_enum):                                      #   enum comedi_conversion_direction
                                                                                #   {
    COMEDI_TO_PHYSICAL = 0                                                      #       COMEDI_TO_PHYSICAL,
    COMEDI_FROM_PHYSICAL = 1                                                    #       COMEDI_FROM_PHYSICAL
                                                                                #   };



##############################################################################
# enum comedi_io_direction
#
#   A comedi_io_direction is used to select between input or output. For 
#   example, comedi_dio_config uses the COMEDI_INPUT and COMEDI_OUTPUT values 
#   to specify whether a configurable digital i/o channel should be configured 
#   as an input or output. 

class comedi_io_direction(c_enum):                                              #   enum comedi_io_direction
                                                                                #   {
    COMEDI_INPUT = 0                                                            #       COMEDI_INPUT,
    COMEDI_OUTPUT = 1                                                           #       COMEDI_OUTPUT
                                                                                #   };

##############################################################################
# enum comedi_subdevice_type
#
#   The comedi_subdevice_type enumeration specifies the possible values for a 
#   subdevice type. These values are used by the functions 
#   comedi_get_subdevice_type and comedi_find_subdevice_by_type. 


class comedi_subdevice_type(c_enum):                                            #    enum comedi_subdevice_type {
    COMEDI_SUBD_UNUSED = 0                                                      #        COMEDI_SUBD_UNUSED,	/* subdevice is unused by driver */
    COMEDI_SUBD_AI = 1                                                          #        COMEDI_SUBD_AI,	/* analog input */
    COMEDI_SUBD_AO = 2                                                          #        COMEDI_SUBD_AO,	/* analog output */
    COMEDI_SUBD_DI = 3                                                          #        COMEDI_SUBD_DI,	/* digital input */
    COMEDI_SUBD_DO = 4                                                          #        COMEDI_SUBD_DO,	/* digital output */
    COMEDI_SUBD_DIO = 5                                                         #        COMEDI_SUBD_DIO,	/* digital input/output */
    COMEDI_SUBD_COUNTER = 6                                                     #        COMEDI_SUBD_COUNTER,	/* counter */
    COMEDI_SUBD_TIMER = 7                                                       #        COMEDI_SUBD_TIMER,	/* timer */
    COMEDI_SUBD_MEMORY = 8                                                      #        COMEDI_SUBD_MEMORY,	/* memory, EEPROM, DPRAM */
    COMEDI_SUBD_CALIB = 9                                                       #        COMEDI_SUBD_CALIB,	/* calibration DACs and pots*/
    COMEDI_SUBD_PROC = 10                                                       #        COMEDI_SUBD_PROC,	/* processor, DSP */
    COMEDI_SUBD_SERIAL = 11                                                     #        COMEDI_SUBD_SERIAL,	/* serial IO */
    COMEDI_SUBD_PWM = 12                                                        #        COMEDI_SUBD_PWM	/* pulse width modulation */
                                                                                #    };

##############################################################################
# enum comedi_oor_behavior

class comedi_oor_behavior(c_enum):                                              #   enum comedi_oor_behavior {
    COMEDI_OOR_NUMBER = 0                                                       #       COMEDI_OOR_NUMBER = 0,
    COMEDI_OOR_NAN = 1                                                          #       COMEDI_OOR_NAN
                                                                                #   };

COMEDI_OOR_NUMBER = comedi_oor_behavior(0)
COMEDI_OOR_NAN = comedi_oor_behavior(1)

##############################################################################
# enum comedi_conversion_direction

class comedi_conversion_direction(c_enum):                                      #   enum comedi_conversion_direction {
    COMEDI_TO_PHYSICAL = 0                                                      #       COMEDI_TO_PHYSICAL,
    COMEDI_FROM_PHYSICAL = 1                                                    #       COMEDI_FROM_PHYSICAL
                                                                                #   };
COMEDI_TO_PHYSICAL = comedi_conversion_direction(0)
COMEDI_FROM_PHYSICAL = comedi_conversion_direction(1)

##############################################################################
# comedi_devinfo
#
#    The data type comedi_devinfo is used to store information about a device. 
#   This structure is usually filled in automatically when the driver is loaded 
#   (“attached”), so programmers need not access this data structure directly.
#     

class _comedi_devinfo_struct(Structure):                			      	#	struct comedi_devinfo_struct {
    _fields_ = [("version_code", c_uint),                                       #		unsigned int version_code;
               ("n_subdevs", c_uint),                                           #		unsigned int n_subdevs;
                ("driver_name", c_char * COMEDI_NAMELEN),                       #		char driver_name[COMEDI_NAMELEN];
                ("board_name", c_char * COMEDI_NAMELEN),                        #		char board_name[COMEDI_NAMELEN];
                ("read_subdevice", c_int),                                      #		int read_subdevice;
                ("write_subdevice", c_int),                                     #		int write_subdevice;
                ("unused", c_int * 30)]                                         #		int unused[30];

if (typedef):
    comedi_devinfo = _comedi_devinfo_struct                                     #     typedef struct comedi_devinfo_struct comedi_devinfo;


##############################################################################
# sampl_t
#    
#   The data type sampl_t is one of the generic types used to represent data 
#   values in Comedilib. It is used in a few places where a data type shorter 
#   than lsampl_t is useful. On most architectures it is a 16-bit, unsigned 
#   integer.
#    
#   Most drivers represent data transferred by read and write functions using 
#   sampl_t. Applications should check the subdevice flag SDF_LSAMPL to 
#   determine if the subdevice uses sampl_t or lsampl_t.

if (typedef):
    lsampl_t = c_uint                                                           #     typedef unsigned int lsampl_t;



##############################################################################
# lsampl_t
#
#    The data type lsampl_t is the data type typically used to represent data 
#    values in Comedilib. On most architectures it is a 32-bit, unsigned integer. 


if (typedef):
    sampl_t = c_ushort                                                          #     typedef unsigned short sampl_t;


##############################################################################
# comedi_range
#
#   The comedi_range structure conveys part of the information necessary to 
#   translate sample values to physical units, in particular, the endpoints of 
#   the range and the physical unit type. The physical unit type is specified 
#   by the field unit, which may take the values UNIT_volt for volts, UNIT_mA 
#   for milliamps, or UNIT_none for unitless. The endpoints are specified by 
#   the fields min and max. 

 
class _comedi_range_struct(Structure):                                          #    typedef struct{                
    _fields_ = [("min", c_double),                                              #        	double min;         
               ("max", c_double),                                               #        	double max;         
                ("unit", c_uint)]                                               #        	unsigned int unit;  
                                                                                #    }comedi_range;                 

if (typedef):
    comedi_range = _comedi_range_struct                                         #    typedef struct comedi_range_struct comedi_range;



##############################################################################
# comedi_krange
#
#   The comedi_krange structure is used to transfer range information between 
#   the driver and Comedilib, and should not normally be used by applications. 
#   The structure conveys the same information as the comedi_range structure, 
#   except the fields min and max are integers, multiplied by a factor of 
#   1000000 compared to the counterparts in comedi_range.
#
#   In addition, kcomedilib uses the comedi_krange structure in place of the 
#   comedi_range structure.



class _comedi_krange_struct(Structure):                                         #   struct comedi_krange_struct{
    _fields_ = [("min", c_int),                                                 #       int min;
                ("max", c_int),                                                 #       int max;
                ("flags", c_uint)]                                              #       unsigned int flags;
                                                                                #   };

if typedef:                                                                     #   typedef struct comedi_krange_struct comedi_krange;
    comedi_krange = _comedi_krange_struct
    
    
    
##############################################################################
# comedi_cmd
#    
#    More information on using commands can be found in the command section. 


class _comedi_cmd_struct(Structure):                                            #	struct comedi_cmd_struct { 
    _fields_ = [("subdev", c_uint),                                             #		unsigned int subdev; 
               ("flags", c_uint),                                               #		unsigned int flags; 
                                                                                #   
                ("start_src", c_uint),                                          #		unsigned int start_src;
                ("start_arg", c_uint),                                          #		unsigned int start_arg;
                                                                                #
                ("scan_begin_src", c_uint),                                     #		unsigned int scan_begin_src;
                ("scan_begin_arg", c_uint),                                     #		unsigned int scan_begin_arg;
                                                                                #
                ("convert_src", c_uint),                                        #		unsigned int convert_src;
                ("convert_arg", c_uint),                                        #		unsigned int convert_arg;
                                                                                #
                ("scan_end_src", c_uint),                                       #		unsigned int scan_end_src;
                ("scan_end_arg", c_uint),                                       #		unsigned int scan_end_arg;
                                                                                #
                ("stop_src", c_uint),                                           #		unsigned int stop_src;
                ("stop_arg", c_uint),                                           #		unsigned int stop_arg;
                                                                                #
                ("chanlist", POINTER(c_uint)),                                  #		unsigned int *chanlist;   	/* channel/range list */
                ("chanlist_len", c_uint),                                       #		unsigned int chanlist_len;
                                                                                #
                ("data", POINTER(sampl_t)),                                     #		sampl_t *data;	/* data list, size depends on subd flags */
                ("data_len", c_uint)]                                           #		unsigned int data_len;
                                                                                #	};

if (typedef):
    	comedi_cmd = _comedi_cmd_struct                                           #    typedef struct comedi_cmd_struct comedi_cmd;


##############################################################################
# subdevice
#
#

class _subdevice_struct(Structure):                                             #    struct subdevice_struct{ 
    _fields_ = [("type", c_uint),                                               #        	unsigned int type;
               ("n_chan", c_uint),                                              #        	unsigned int n_chan;
                ("subd_flags", c_uint),                                         #        	unsigned int subd_flags;
                ("timer_type", c_uint),                                         #        	unsigned int timer_type;
                ("len_chanlist", c_uint),                                       #        	unsigned int len_chanlist;
                ("maxdata", lsampl_t),                                          #        	lsampl_t maxdata;
                ("flags", c_uint),                                              #        	unsigned int flags;
                ("range_type", c_uint),                                         #        	unsigned int range_type;
                                                                                #  
                ("maxdata_list", POINTER(lsampl_t)),                            #        	lsampl_t *maxdata_list;
                ("range_type_list", POINTER(c_uint)),                           #        	unsigned int *range_type_list;
                ("flags_list", POINTER(c_uint)),                                #        	unsigned int *flags_list;     
                                                                                #    
                ("rangeinfo", POINTER(_comedi_range_struct)),                   #        	comedi_range *rangeinfo; 
                ("rangeinfo_list", POINTER(POINTER(_comedi_range_struct))),     #        	comedi_range **rangeinfo_list; 
                                                                                #  
                ("has_cmd", c_uint),                                            #        	unsigned int has_cmd; 
                ("has_insn_bits", c_uint),                                      #        	unsigned int has_insn_bits; 
                                                                                #  
                ("cmd_has_errno", c_int),                                       #        	int cmd_mask_errno;
                ("cmd_mask", POINTER(_comedi_cmd_struct)),                      #        	comedi_cmd *cmd_mask;
                ("cmd_timed_errno", c_int),                                     #        	int cmd_timed_errno;
                ("cmd_timed", POINTER(_comedi_cmd_struct))]                     #        	comedi_cmd *cmd_timed;
                                                                                #     };

if (typedef):
    subdevice = _subdevice_struct                                               #     typedef struct subdevice_struct subdevice;


##############################################################################
# comedi_t
#  
#    The data type comedi_t is used to represent an open Comedi device
#    
#    A valid comedi_t pointer is returned by a successful call to comedi_open, 
#   and should be used for subsequent access to the device. It is an opaque 
#   type, and pointers to type comedi_t should not be dereferenced by the 
#   application. 

class _comedi_t_struct(Structure):                                              #    struct comedi_t_struct{
    _fields_ = [("magic", c_int),                                               #        	int magic;
                                                                                #        
               ("fd", c_int),                                                   #        	int fd;
                ("n_subdevices", c_int),                                        #        	int n_subdevices;
                                                                                #        
                ("devinfo", _comedi_devinfo_struct),                            #        	comedi_devinfo devinfo;
                                                                                #        
                ("subdevices", POINTER(_subdevice_struct)),                     #        	subdevice *subdevices;
                                                                                #        
                ("has_insnlist_ioctl", c_uint),                                 #        	unsigned int has_insnlist_ioctl;
                ("has_insn_ioctl", c_uint)]                                     #        	unsigned int has_insn_ioctl;
                                                                                #     };

if (typedef):
    comedi_t = _comedi_t_struct                                                 #     typedef struct comedi_t_struct comedi_t;


##############################################################################
# comedi_insn
#
#   Comedi instructions are described by the comedi_insn structure. 
#   Applications send instructions to the driver in order to perform control 
#   and measurement operations that are done immediately or synchronously, 
#   i.e., the operations complete before program control returns to the 
#   application. In particular, instructions cannot describe acquisition that 
#   involves timers or external events.
#
#   The field insn determines the type of instruction that is sent to the 
#   driver. Valid instruction types are:
#
#   INSN_READ       read values from an input channel 
#   INSN_WRITE      write values to an output channel 
#   INSN_BITS       read/write values on multiple digital I/O channels 
#   INSN_CONFIG     configure a subdevice 
#   INSN_GTOD       read a timestamp, identical to gettimeofday except the 
#                    seconds and microseconds values are of type lsampl_t. 
#   INSN_WAIT       wait a specified number of nanoseconds 
#
#   The number of samples to read or write, or the size of the configuration 
#   structure is specified by the field n, and the buffer for those samples by 
#   data. The field subdev is the subdevice index that the instruction is sent 
#   to. The field chanspec specifies the channel, range, and analog reference 
#   (if applicable).
#
#   Instructions can be sent to drivers using comedi_do_insn. Multiple 
#   instructions can be sent to drivers in the same system call using 
#   comedi_do_insnlist. 


class _comedi_insn_struct(Structure):                                           #   struct comedi_insn_struct{
    _fields_ = [("insn", c_uint),                                               #       unsigned int insn;
                ("n", c_uint),                                                  #       unsigned int n;
                ("data", POINTER(lsampl_t)),                                    #       lsampl_t*data;
                ("subdev", c_uint),                                             #       unsigned int subdev;
                ("chanspec", c_uint),                                           #       unsigned int chanspec;
                ("unused", c_uint * 3)]                                         #       unsigned int unused[3];
                                                                                #   };


if typedef:                                                                     #   typedef struct comedi_insn_struct comedi_insn;
    comedi_insn = _comedi_insn_struct
    
    
##############################################################################
# comedi_insnlist
#
#   A comedi_insnlist structure is used to communicate a list of instructions 
#   to the driver using the comedi_do_insnlist function.

class _comedi_insnlist_struct(Structure):                                       #   struct comedi_insnlist_struct{
    _fields_ = [("n_insns", c_uint),                                            #       unsigned int n_insns;
                ("insns", POINTER(_comedi_insn_struct))]                        #       comedi_insn *insns;
                                                                                #   };

if typedef:                                                                     #   typedef struct comedi_insnlist_struct comedi_insnlist;
    comedi_insnlist = _comedi_insnlist_struct
    



##############################################################################
# COMEDILIB_STRICT_ABI Definitions
#   - structs and functions used for parsing calibration files 
##############################################################################
#/*
#   The following prototypes are _NOT_ part of the Comedilib ABI, and
#   may change in future versions without regard to source or binary
#   compatibility.  In practice, this is a holding place for the next
#   library ABI version change.
# */


    
##############################################################################
# comedi_polynomial_t
#
#   A comedi_polynomial_t holds calibration data for a channel of a subdevice. 
#   It is initialized by the comedi_get_hardcal_converter or 
#   comedi_get_softcal_converter calibration functions and is passed to the 
#   comedi_to_physical and comedi_from_physical raw/physical conversion 
#   functions. 
#

class _comedi_polynomial_t(Structure):                                          #   typedef struct {
    _fields_ = [("coefficients", c_double * COMEDI_POLYNOMIAL_COEFFS.value),    #       double coefficients[COMEDI_MAX_NUM_POLYNOMIAL_COEFFICIENTS];
                ("expansion_origin", c_double),                                 #       double expansion_origin;
                ("order", c_uint)]                                              #       unsigned order;
if typedef:                                                                     #   } comedi_polynomial_t;
    comedi_polynomial_t = _comedi_polynomial_t



##############################################################################
# comedi_caldac_t

class _comedi_caldac_t(Structure):                                              #   class _comedi_caldac_t typedef struct {
    _fields_ = [("subdevice", c_uint),                                          #       unsigned int subdevice;
                ("channel", c_uint),                                            #       unsigned int channel;
                ("value", c_uint)]                                              #       unsigned int value;
                                                                                #   } comedi_caldac_t;

if strict_abi:
    comedi_caldac_t = _comedi_caldac_t


##############################################################################
# comedi_softcal_t

class _comedi_softcal_t(Structure):                                             #   typedef struct {
    _fields_ = [("to_phys", POINTER(_comedi_polynomial_t)),                     #       comedi_polynomial_t *to_phys;
                ("from_phys", POINTER(_comedi_polynomial_t))]                   #       comedi_polynomial_t *from_phys;
                                                                                #   } comedi_softcal_t;

if strict_abi:
    comedi_softcal_t = _comedi_softcal_t

##############################################################################
# comedi_calibration_setting_t

class _comedi_calibration_setting_t(Structure):                                 #   typedef struct {
    _fields_ = [("subdevice", c_uint),                                          #       unsigned int subdevice;
                ("channels", POINTER(c_uint)),                                  #       unsigned int *channels;
                ("num_channels", c_uint),                                       #       unsigned int num_channels;
                ("ranges", POINTER(c_uint)),                                    #       unsigned int *ranges;
                ("num_ranges", c_uint),                                         #       unsigned int num_ranges;
                ("arefs", c_uint * CS_MAX_AREFS_LENGTH),                        #       unsigned int arefs[ CS_MAX_AREFS_LENGTH ];
                ("num_arefs", c_uint),                                          #       unsigned int num_arefs;
                ("caldacs", POINTER(_comedi_caldac_t)),                         #       comedi_caldac_t *caldacs;
                ("num_caldacs", c_uint),                                        #       unsigned int num_caldacs;
                ("soft_calibration", _comedi_softcal_t)]                        #       comedi_softcal_t soft_calibration;
                                                                                #   } comedi_calibration_setting_t;

if strict_abi:
    comedi_calibration_setting_t = _comedi_calibration_setting_t

##############################################################################
# comedi_calibration_t

class _comedi_calibration_t(Structure):                                         #   typedef struct {
    _fields_ = [("driver_name", c_char_p),                                      #       char *driver_name;
                ("board_name", c_char_p),                                       #       char *board_name;
                ("settings", POINTER(_comedi_calibration_setting_t)),           #       comedi_calibration_setting_t *settings;
                ("num_settings", c_uint) ]                                      #       unsigned int num_settings;
                                                                                #   } comedi_calibration_t;
if typedef:
    comedi_calibration_t = _comedi_calibration_t



##############################################################################
# comedi_sv_struct


class _comedi_sv_struct(Structure):                                             #   typedef struct comedi_sv_struct{
    _fields_ = [("dev", POINTER(comedi_t)),                                     #       comedi_t *dev;
                ("subdevice", c_uint),                                          #       unsigned int subdevice;
                ("chan", c_uint),                                               #       unsigned int chan;
                ("range", c_int),                                               #       int range; /* range policy */
                ("aref", c_int),                                                #       int aref;
                ("n", c_int),                                                   #       int n; /* number of measurements to average (for ai) */
                ("maxdata", lsampl_t)]                                          #       lsampl_t maxdata;
                                                                                #   } comedi_sv_t;

if typedef:
    comedi_sv_t = _comedi_sv_struct



##############################################################################
# comedi_trig_struct

class _comedi_trig_struct(Structure):                                           #    struct comedi_trig_struct {
    _fields_ = [ ("subdev", c_uint),                                            #        unsigned int subdev;	/* subdevice */
                 ("mode", c_uint),                                              #        unsigned int mode;	/* mode */
                 ("flags", c_uint),                                             #        unsigned int flags;
                 ("n_chan", c_uint),                                            #        unsigned int n_chan;	/* number of channels */
                 ("chanlist", POINTER(c_uint)),                                 #        unsigned int *chanlist;	/* channel/range list */
                 ("data", POINTER(sampl_t)),                                    #        sampl_t *data;	/* data list, size depends on subd flags */
                 ("n", c_uint),                                                 #        unsigned int n;	/* number of scans */
                 ("trigsrc", c_uint),                                           #        unsigned int trigsrc;
                 ("trigvar", c_uint),                                           #        unsigned int trigvar;
                 ("trigvarl", c_uint),                                          #        unsigned int trigvar1;
                 ("data_len", c_uint),                                          #        unsigned int data_len;
                 ("unused", c_uint * 3) ]                                       #        unsigned int unused[3];
                                                                                #   };

if typedef:
    comedi_trig = _comedi_trig_struct                                           #   typedef struct comedi_trig_struct comedi_trig;



##############################################################################
#                   - Begin CORE FUNCTIONS section -
##############################################################################


# using _grab to get address of named C function and place it in a "_FuncPtr" 
_grab = _libcomedi.__getitem__

# Import stdout.write as printf()
from sys import stdout as _stdout
printf = _stdout.write


##############################################################################
# comedi_close — close a Comedi device
#
#   include <comedilib.h>
#
#   int comedi_close(	comedi_t * device);
# 
# Description
#
#   Close a device previously opened by comedi_open.
#
# Return value
#
#   If successful, comedi_close returns 0. On failure, -1 is returned. 

comedi_close = _grab("comedi_close")
comedi_close.restype = c_int                                                    #   int comedi_close(
comedi_close.argtypes = [ POINTER(comedi_t) ]                                   #       comedi_t *it );


##############################################################################
# comedi_data_read — read single sample from channel
#
#   #include <comedilib.h>
#
#   int comedi_data_read(	comedi_t * device,
#       unsigned int subdevice,
#       unsigned int channel,
#       unsigned int range,
#       unsigned int aref,
#       lsampl_t * data);
# 
# Description
#
#   Reads a single sample on the channel specified by the Comedi device device, 
#   the subdevice subdevice, and the channel channel. For the A/D conversion 
#   (if appropriate), the device is configured to use range specification range
#   and (if appropriate) analog reference type aref. Analog reference types 
#   that are not supported by the device are silently ignored.
#
#   The function comedi_data_read reads one data value from the specified 
#   channel and stores the value in *data.

#   WARNING: comedi_data_read does not do any pausing to allow multiplexed 
#   analog inputs to settle before starting an analog to digital conversion. 
#   If you are switching between different channels and need to allow your 
#   analog input to settle for an accurate reading, use 
#   comedi_data_read_delayed, or set the input channel at an earlier time with 
#   comedi_data_read_hint.
#
#   Data values returned by this function are unsigned integers less than or 
#   equal to the maximum sample value of the channel, which can be determined 
#   using the function comedi_get_maxdata. Conversion of data values to 
#   physical units can be performed by the functions comedi_to_phys (linear 
#   conversion) or comedi_to_physical (non-linear polynomial conversion).
#
# Return value
#
#   On success, comedi_data_read returns 1 (the number of samples read). If 
#   there is an error, -1 is returned. 

comedi_data_read = _grab("comedi_data_read")
comedi_data_read.restype = c_int                                                #   int comedi_data_read(
comedi_data_read.argtypes = [ POINTER(comedi_t),                                #       comedi_t * device,
                              c_uint,                                           #       unsigned int subdevice,
                              c_uint,                                           #       unsigned int channel,
                              c_uint,                                           #       unsigned int range,
                              c_uint,                                           #       unsigned int aref,
                              POINTER(lsampl_t) ]                               #       lsampl_t * data);



##############################################################################
# comedi_data_read_n — read multiple samples from channel
#
#   #include <comedilib.h>
#
#   int comedi_data_read_n(	comedi_t * device,
#       unsigned int subdevice,
#       unsigned int channel,
#       unsigned int range,
#       unsigned int aref,
#       lsampl_t * data,
#       unsigned int n);
# 
# Description
#
#   Similar to comedi_data_read except it reads n samples into the array data. 
#   The precise timing of the samples is not hardware controlled.

comedi_data_read_n = _grab("comedi_data_read_n")
comedi_data_read_n.restype = c_int                                              #   int comedi_data_read_n(	comedi_t * device,
comedi_data_read_n.argtypes = [ c_uint,                                         #       unsigned int subdevice,
                                c_int,                                          #       unsigned int channel,
                                c_int,                                          #       unsigned int range,
                                c_int,                                          #       unsigned int aref,
                                POINTER(lsampl_t),                              #       lsampl_t * data,
                                c_uint ]                                        #       unsigned int n);



##############################################################################
# comedi_data_read_delayed — read single sample from channel after delaying 
#                             for specified settling time
#
#   #include <comedilib.h>
#
#   int comedi_data_read_delayed(	comedi_t * device,
#       unsigned int subdevice,
#       unsigned int channel,
#       unsigned int range,
#       unsigned int aref,
#       lsampl_t * data,
#       unsigned int nanosec);
# 
# Description
#
#   Similar to comedi_data_read except it will wait for the specified number 
#   of nanoseconds between setting the input channel and taking a sample. For 
#   analog inputs, most boards have a single analog to digital converter which 
#   is multiplexed to be able to read multiple channels. If the input is not 
#   allowed to settle after the multiplexer switches channels, the reading will 
#   be inaccurate. This function is useful for allowing a multiplexed analog 
#   input to settle when switching channels.
#
#   Although the settling time is specified in nanoseconds, the actual settling
#   time will be rounded up to the nearest microsecond. 

comedi_data_read_delayed = _grab("comedi_data_read_delayed")
comedi_data_read_delayed.restype = c_int                                        #   int comedi_data_read_delayed(	
comedi_data_read_delayed.argtypes = [ POINTER(comedi_t),                        #       comedi_t * device,
                                      c_uint,                                   #       unsigned int subdevice,
                                      c_uint,                                   #       unsigned int channel,
                                      c_uint,                                   #       unsigned int range,
                                      c_uint,                                   #       unsigned int aref,
                                      POINTER(lsampl_t),                        #       lsampl_t * data,
                                      c_uint ]                                  #       unsigned int nanosec);


##############################################################################
# comedi_data_read_hint — tell driver which channel/range/aref you are going 
#                          to read from next
#
#   #include <comedilib.h>
#
#   int comedi_data_read_hint(	comedi_t * device,
#       unsigned int subdevice,
#       unsigned int channel,
#       unsigned int range,
#       unsigned int aref);
# 
# Description
#
#   Used to prepare an analog input for a subsequent call to comedi_data_read. 
#   It is not necessary to use this function, but it can be useful for 
#   eliminating inaccuracies caused by insufficient settling times when 
#   switching the channel or gain on an analog input. This function sets an 
#   analog input to the channel, range, and aref specified but does not 
#   perform an actual analog to digital conversion.
#
#   Alternatively, one can simply use comedi_data_read_delayed, which sets up 
#   the input, pauses to allow settling, then performs a conversion. 

comedi_data_read_hint = _grab("comedi_data_read_hint")
comedi_data_read_hint.restype = c_int                                           #   int comedi_data_read_hint(
comedi_data_read_hint.argtypes = [ POINTER(comedi_t),                           #       comedi_t * device,
                                   c_uint,                                      #       unsigned int subdevice,
                                   c_uint,                                      #       unsigned int channel,
                                   c_uint,                                      #       unsigned int range,
                                   c_uint ]                                     #       unsigned int aref);
                                  



##############################################################################
# comedi_data_write — write single sample to channel
#
#   #include <comedilib.h>
#
#   int comedi_data_write(	comedi_t * device,
#       unsigned int subdevice,
#       unsigned int channel,
#       unsigned int range,
#       unsigned int aref,
#       lsampl_t data);
# 
# Description
#
#   Writes a single sample on the channel that is specified by the Comedi 
#   device device, the subdevice subdevice, and the channel channel. If 
#   appropriate, the device is configured to use range specification range 
#   and analog reference type aref. Analog reference types that are not 
#   supported by the device are silently ignored.
#
#   The function comedi_data_write writes the data value specified by the 
#   parameter data to the specified channel.
#
# Return value
#
#   On success, comedi_data_write returns 1 (the number of samples written). 
#   If there is an error, -1 is returned.

comedi_data_write = _libcomedi.comedi_data_write
comedi_data_write.restype = c_int                                               #   int comedi_data_write(
comedi_data_write.argtypes = [ POINTER(comedi_t),                               #       comedi_t * device,
                               c_uint,                                          #       unsigned int subdevice,
                               c_uint,                                          #       unsigned int channel,
                               c_uint,                                          #       unsigned int range,
                               c_uint,                                          #       unsigned int aref,
                               lsampl_t ]                                       #       lsampl_t data);



##############################################################################
# comedi_do_insn — perform instruction
#
#   #include <comedilib.h>
#
#   int comedi_do_insn(	comedi_t * device,
#       comedi_insn * instruction);
# 
# Description
#
#   The function comedi_do_insn performs a single instruction.
#
# Return value
#
#   If successful, returns a non-negative number. For the case of INSN_READ or 
#   INSN_WRITE instructions, comedi_do_insn returns the number of samples read 
#   or written, which may be less than the number requested. If there is an 
#   error, -1 is returned. 

comedi_do_insn = _grab("comedi_do_insn")
comedi_do_insn.restype = c_int                                                  #   int comedi_do_insn(
comedi_do_insn.argtypes = [ POINTER(comedi_t),                                  #       comedi_t * device,
                            POINTER(comedi_insn) ]                              #       comedi_insn * instruction);
 
 
 
##############################################################################
# comedi_do_insnlist — perform multiple instructions
#
#   #include <comedilib.h>
#
#   int comedi_do_insnlist(	comedi_t * device,
#       comedi_insnlist * list);
# 
# Description
#
#   The function comedi_do_insnlist performs multiple Comedi instructions as 
#   part of one system call. This function can be used to avoid the overhead 
#   of multiple system calls.
#
# Return value
#
#   The function comedi_do_insnlist returns the number of successfully 
#   completed instructions. Error information for the unsuccessful 
#   instruction is not available. If there is an error before the first 
#   instruction can be executed, -1 is returned.

comedi_do_insnlist = _grab("comedi_do_insnlist")
comedi_do_insnlist.restype = c_int                                              #   int comedi_do_insnlist(
comedi_do_insnlist.argtypes = [ POINTER(comedi_t),                              #       comedi_t * device,
                                POINTER(comedi_insnlist) ]                      #       comedi_insnlist * list);


##############################################################################
# comedi_fileno — get file descriptor for open Comedilib device
#
#   #include <comedilib.h>
#
#   int comedi_fileno(	comedi_t * device);
#
# Description
#
#   The function comedi_fileno returns the file descriptor for the device 
#   device. This descriptor can then be used as the file descriptor parameter 
#   of read, write, etc. This function is intended to mimic the standard C 
#   library function fileno.
#
#   The returned file descriptor should not be closed, and will become invalid 
#   when comedi_close is called on device.
#
# Return value
#
#   A file descriptor, or -1 on error. 

comedi_fileno = _grab("comedi_fileno")
comedi_fileno.restype = c_int                                                   #   int comedi_fileno(
comedi_fileno.argtypes = [ POINTER(comedi_t) ]                                  #   comedi_t * device);


##############################################################################
# comedi_find_range — search for range
#
#   #include <comedilib.h>
#
#   int comedi_find_range(	comedi_t * device,
#       unsigned int subdevice,
#       unsigned int channel,
#       unsigned int unit,
#       double min,
#       double max);
#
# Description
#
#   The function comedi_find_range tries to locate the optimal (smallest) 
#   range for the channel channel belonging to subdevice subdevice of the 
#   comedi device device, that includes both min and max in units of unit.
#
# Return value
#
#   If a matching range is found, the index of the matching range is returned. 
#   If no matching range is available, the function returns -1. 

comedi_find_range = _grab("comedi_find_range")
comedi_find_range.restype = c_int                                               #   int comedi_find_range(
comedi_find_range.argtypes = [ POINTER(comedi_t),                               #  comedi_t * device,
                               c_uint,                                          #       unsigned int subdevice,
                               c_uint,                                          #       unsigned int channel,
                               c_uint,                                          #       unsigned int unit,
                               c_double,                                        #       double min,
                               c_double ]                                       #       double max);


##############################################################################
# comedi_find_subdevice_by_type — search for subdevice type
#
#   #include <comedilib.h>
#
#   int comedi_find_subdevice_by_type(	comedi_t * device,
#       int type,
#       unsigned int start_subdevice);
#
# Description
#
#   The function comedi_find_subdevice_by_type tries to locate a subdevice 
#   belonging to comedi device device, having type type, starting with the 
#   subdevice start_subdevice. The comedi_subdevice_type enum specifies the 
#   possible subdevice types.
#
# Return value
#
#   If it finds a subdevice with the requested type, it returns its index. If 
#   there is an error, the function returns -1 and sets the appropriate error. 

comedi_find_subdevice_by_type = _grab("comedi_find_subdevice_by_type")
comedi_find_subdevice_by_type.restype = c_int                                   #   int comedi_find_subdevice_by_type(
comedi_find_subdevice_by_type.argtypes = [ POINTER(comedi_t),                   #       comedi_t * device,
                                           c_int,                               #       int type,
                                           c_uint ]                             #       unsigned int start_subdevice);
                                           

##############################################################################
# comedi_from_phys — convert physical units to sample
#
#   #include <comedilib.h>
#
#   lsampl_t comedi_from_phys(	double data,
#       comedi_range * range,
#       lsampl_t maxdata);
#
# Description
#
#   Converts parameter data given in physical units (double) into sample 
#   values (lsampl_t, between 0 and maxdata). The parameter range represents 
#   the conversion information to use, and the parameter maxdata represents 
#   the maximum possible data value for the channel that the data will be 
#   written to. The mapping between physical units and raw data is linear 
#   and assumes that the converter has ideal characteristics.
#
#   Conversion is not affected by out-of-range behavior. Out-of-range data 
#   parameters are silently truncated to the range 0 to maxdata. 

comedi_from_phys = _grab("comedi_from_phys")
comedi_from_phys.restype = lsampl_t                                             #   lsampl_t comedi_from_phys(
comedi_from_phys.argtypes = [ c_double,                                         #   double data,
                              POINTER(comedi_range),                            #   comedi_range * range,
                              lsampl_t ]                                        #   lsampl_t maxdata
                              

##############################################################################
# comedi_from_physical — convert physical units to sample using calibration data
#
#
#   #include <comedilib.h>
#
#   lsampl_t comedi_from_physical(	double data,
#       const comedi_polynomial_t * conversion_polynomial);
# 
# Description
#
#   Converts data given in physical units into Comedi's integer sample values 
#   (lsampl_t, between 0 and maxdata — see comedi_get_maxdata). The 
#   conversion_polynomial parameter is obtained from either 
#   comedi_get_hardcal_converter or comedi_get_softcal_converter. The allows 
#   non linear and board specific correction. The result will be rounded using 
#   the C library's current rounding direction. No range checking of the input 
#   data is performed. It is up to you to ensure your data is within the 
#   limits of the output range you are using.
#
# Return value
#
#   Comedi sample value corresponding to input physical value. 


comedi_from_physical = _grab("comedi_from_physical")
comedi_from_physical.restype = lsampl_t                                         #   lsampl_t comedi_from_physical(	
comedi_from_physical.argtypes = [ c_double,                                     #       double data,
                                  POINTER(comedi_polynomial_t) ]                #       const comedi_polynomial_t * conversion_polynomial);
                                  #      |                                                |
                                  #      └--------------- no const in python -------------┘
                                  

##############################################################################
# comedi_get_board_name — Comedi device name
#
#   #include <comedilib.h>
#
#   const char * comedi_get_board_name(	comedi_t * device);
# 
# Description
#
#   The function comedi_get_board_name returns a pointer to a string containing
#   the name of the comedi device represented by device. This pointer is valid 
#   until the device is closed. This function returns NULL if there is an error. 

comedi_get_board_name = _grab("comedi_get_board_name")
comedi_get_board_name.restype = c_char_p                                        #   const char * comedi_get_board_name(	
comedi_get_board_name.argtypes = [ POINTER(comedi_t) ]                          #       comedi_t * device);


##############################################################################
# comedi_get_driver_name — Comedi driver name
#
#   #include <comedilib.h>
#
#   char * comedi_get_driver_name(	comedi_t * device);
#
# Description
#
#   The function comedi_get_driver_name returns a pointer to a string 
#   containing the name of the driver being used by comedi for the comedi 
#   device represented by device. This pointer is valid until the device is 
#   closed. This function returns NULL if there is an error.

comedi_get_driver_name = _grab("comedi_get_board_name")                         
comedi_get_driver_name.restype = c_char_p                                       #   char * comedi_get_driver_name(
comedi_get_driver_name.argtypes = [ POINTER(comedi_t) ]                         #       comedi_t * device);



##############################################################################
# comedi_get_maxdata — maximum sample of channel
#
#   #include <comedilib.h>
#
#   lsampl_t comedi_get_maxdata(	comedi_t * device,
#       unsigned int subdevice,
#       unsigned int channel);
#
# Description
#
#   The function comedi_get_maxdata returns the maximum valid data value for 
#   channel channel of subdevice subdevice belonging to the comedi device 
#   device.
#
# Return value
#
#   The maximum valid sample value, or 0 on error. 


comedi_get_maxdata = _grab("comedi_get_maxdata")                                
comedi_get_maxdata.restype = lsampl_t                                           #   lsampl_t comedi_get_maxdata(
comedi_get_maxdata.argtypes = [ POINTER(comedi_t),                              #       comedi_t * device,
                                c_uint,                                         #       unsigned int subdevice,
                                c_uint ]                                        #       unsigned int channel);


##############################################################################
# comedi_get_n_channels — number of subdevice channels
#
#   #include <comedilib.h>
#
#   int comedi_get_n_channels(	comedi_t * device,
#       unsigned int subdevice);
#
# Description
#
#   The function comedi_get_n_channels returns the number of channels of the 
#   subdevice subdevice belonging to the comedi device device. This function 
#   returns -1 on error and the Comedilib error value is set. 

comedi_get_n_channels = _grab("comedi_get_n_channels")
comedi_get_n_channels.restype = c_int                                           #   int comedi_get_n_channels(
comedi_get_n_channels.argtypes = [ POINTER(comedi_t),                           #       comedi_t * device,
                                   c_uint ]                                     #       unsigned int subdevice);



##############################################################################
# comedi_get_n_ranges — number of ranges of channel
#
#   #include <comedilib.h>
#
#   int comedi_get_n_ranges(	comedi_t * device,
#       unsigned int subdevice,
#       unsigned int channel);
#
# Description
#
#   The function comedi_get_n_ranges returns the number of ranges of the 
#   channel channel belonging to the subdevice subdevice of the comedi device 
#   device. This function returns -1 on error.

comedi_get_n_ranges = _grab("comedi_get_n_ranges")
comedi_get_n_ranges.restype = c_int                                             #   int comedi_get_n_ranges(
comedi_get_n_ranges.argtypes = [ POINTER(comedi_t),                             #       comedi_t * device,
                                 c_uint,                                        #       unsigned int subdevice,
                                 c_uint ]                                       #       unsigned int channel);


##############################################################################
# comedi_get_n_subdevices — number of subdevices
#
#   #include <comedilib.h>
#
#   int comedi_get_n_subdevices(	comedi_t * device);
#
# Description
#
#   The function comedi_get_n_subdevices returns the number of subdevices 
#   belonging to the Comedi device referenced by the parameter device, or -1 
#   on error.

comedi_get_n_subdevices = _grab("comedi_get_n_subdevices")
comedi_get_n_subdevices.restype = c_int                                         #   int comedi_get_n_subdevices(
comedi_get_n_subdevices.argtypes = [ POINTER(comedi_t) ]                        #       comedi_t * device);



##############################################################################
# comedi_get_range — range information of channel
#
#   #include <comedilib.h>
#
#   comedi_range * comedi_get_range(	comedi_t * device,
#       unsigned int subdevice,
#       unsigned int channel,
#       unsigned int range);
#
# Description
#
#   The function comedi_get_range returns a pointer to a comedi_range structure 
#   that contains information on the range specified by the subdevice, channel, 
#   and range parameters. The pointer is valid until the Comedi device device 
#   is closed. If there is an error, NULL is returned.

comedi_get_range = _grab("comedi_get_range")
comedi_get_range.restype = POINTER(comedi_range)                                #   comedi_range * comedi_get_range(
comedi_get_range.argtypes = [ POINTER(comedi_t),                                #       comedi_t * device,
                              c_uint,                                           #       unsigned int subdevice,
                              c_uint,                                           #       unsigned int channel,
                              c_uint ]                                          #       unsigned int range);



##############################################################################
# comedi_get_subdevice_flags — properties of subdevice
#
#   #include <comedilib.h>
#
#   int comedi_get_subdevice_flags(	comedi_t * device,
#       unsigned int subdevice);
#
# Description
#
#   The function comedi_get_subdevice_flags returns a bitfield describing the 
#   capabilities of the specified subdevice subdevice of the Comedi device 
#   device. If there is an error, -1 is returned, and the Comedilib error 
#   value is set.
#
#   Subdevice Flag      Value (hex)     Description
#   SDF_BUSY            0x00000001      The subdevice is busy performing an 
#                                       asynchronous command. A subdevice being
#                                       “busy” is slightly different from the 
#                                       “running” state flagged by SDF_RUNNING. 
#                                       A “running” subdevice is always “busy”, 
#                                       but a “busy” subdevice is not 
#                                       necessarily “running”. For example, 
#                                       suppose an analog input command has 
#                                       been completed by the hardware, but 
#                                       there are still samples in Comedi's 
#                                       buffer waiting to be read out. In this 
#                                       case, the subdevice is not “running”, 
#                                       but is still “busy” until all the 
#                                       samples are read out or comedi_cancel 
#                                       is called.
#
#   SDF_BUSY_OWNER      0x00000002	      The subdevice is “busy”, and the command 
#                                       it is running was started by the current 
#                                       process.
#
#   SDF_LOCKED          0x00000004      The subdevice has been locked by 
#                                       comedi_lock.
#
#   SDF_LOCK_OWNER      0x00000008      The subdevice is locked, and was locked 
#                                       by the current process.
#
#   SDF_MAXDATA         0x00000010      The maximum data value for the 
#                                       subdevice depends on the channel.
#
#   SDF_FLAGS           0x00000020      The subdevice flags depend on the 
#                                       channel (unfinished/broken support in 
#                                       library).
#
#   SDF_RANGETYPE       0x00000040      The range type depends on the channel.
#
#   SDF_CMD             0x00001000      The subdevice supports asynchronous 
#                                       commands.
#   SDF_SOFT_CALIBRATED 0x00002000      The subdevice relies on the host to do 
#                                       calibration in software. Software 
#                                       calibration coefficients are determined 
#                                       by the comedi_soft_calibrate utility. 
#                                       See the description of the 
#                                       comedi_get_softcal_converter function 
#                                       for more information.
#
#   SDF_READABLE        0x00010000      The subdevice can be read (e.g. analog 
#                                       input).
#
#   SDF_WRITABLE        0x00020000      The subdevice can be written to (e.g. 
#                                       analog output).
#
#   SDF_INTERNAL        0x00040000      The subdevice does not have externally 
#                                       visible lines.
#
#   SDF_GROUND          0x00100000      The subdevice supports analog 
#                                       reference AREF_GROUND.
#
#   SDF_COMMON          0x00200000      The subdevice supports analog 
#                                       reference AREF_COMMON.
#
#   SDF_DIFF            0x00400000      The subdevice supports analog 
#                                       reference AREF_DIFF.
#
#   SDF_OTHER           0x00800000      The subdevice supports analog 
#                                       reference AREF_OTHER
#
#   SDF_DITHER          0x01000000      The subdevice supports dithering (via 
#                                       the CR_ALT_FILTER chanspec flag).
#
#   SDF_DEGLITCH        0x02000000      The subdevice supports deglitching 
#                                       (via the CR_ALT_FILTER chanspec flag).
#
#   SDF_RUNNING         0x08000000      An asynchronous command is running. 
#                                       You can use this flag to poll for the 
#                                       completion of an output command.
#
#   SDF_LSAMPL          0x10000000      The subdevice uses the 32-bit lsampl_t 
#                                       type instead of the 16-bit sampl_t for 
#                                       asynchronous command data.
#
#   SDF_PACKED          0x20000000      The subdevice uses bitfield samples for 
#                                       asynchronous command data, one bit per 
#                                       channel (otherwise it uses one sampl_t 
#                                       or lsampl_t per channel). Commonly used 
#                                       for digital subdevices.

comedi_get_subdevice_flags = _grab("comedi_get_subdevice_flags")
comedi_get_subdevice_flags.restype = c_int                                      #   int comedi_get_subdevice_flags(
comedi_get_subdevice_flags.argtypes = [ POINTER(comedi_t),                      #       comedi_t * device,
                                        c_uint ]                                #       unsigned int subdevice);


##############################################################################
# comedi_get_subdevice_type — type of subdevice
#
#   #include <comedilib.h>
#
#   int comedi_get_subdevice_type(	comedi_t * device,
#       unsigned int subdevice);
#
# Description
#
#   The function comedi_get_subdevice_type returns an integer describing the 
#   type of subdevice that belongs to the comedi device device and has the 
#   subdevice index subdevice. The comedi_subdevice_type enum specifies the 
#   possible values for the subdevice type.
#
# Return value
#
#   The function returns the subdevice type, or -1 if there is an error.

comedi_get_subdevice_type = _grab("comedi_get_subdevice_type")
comedi_get_subdevice_type.restype = c_int                                       #   int comedi_get_subdevice_type(
comedi_get_subdevice_type.argyptes = [ POINTER(comedi_t),                       #       comedi_t * device,
                                       c_uint ]                                 #       unsigned int subdevice);



##############################################################################
# comedi_get_version_code — Comedi version code
#
#   #include <comedilib.h>
#
#   int comedi_get_version_code(	comedi_t * device);
#
# Description
#
#   Returns the Comedi kernel module version code. A valid Comedi device 
#   referenced by the parameter device is necessary to communicate with the 
#   kernel module. On error, -1 is returned.
#
#   The version code is encoded as a bitfield of three 8-bit numbers. For 
#   example, 0x00073d is the version code for version 0.7.61.
#
#   This function is of limited usefulness. A typical mis-application of this 
#   function is to use it to determine if a certain feature is supported. If 
#   the application needs to know of the existence of a particular feature, an 
#   existence test function should be written and put in the Comedilib source.

comedi_get_version_code = _grab("comedi_get_version_code")
comedi_get_version_code.restype = c_int                                         #   int comedi_get_version_code(
comedi_get_version_code.argtypes = [ POINTER(comedi_t) ]                        #       comedi_t * device);


##############################################################################
# comedi_internal_trigger — generate soft trigger
#
#   #include <comedilib.h>
#
#   int comedi_internal_trigger(	comedi_t * device,
#       unsigned int subdevice,
#       unsigned int trig_num);
#
# Description
#
#   This function sends an INSN_INTTRIG instruction to a subdevice, which 
#   causes an internal triggering event. This event can, for example, trigger 
#   a subdevice to start an asynchronous command.
#
#   The trig_num parameter is reserved for future use, and should be set to 0. 
#   It is likely it will be used in the future to support multiple independent 
#   internal triggers. For example, an asynchronous command might be specified 
#   for a subdevice with a start_src of TRIG_INT, and a start_arg of 5. Then 
#   the start event would only be triggered if comedi_internal_trigger were 
#   called on the subdevice with a trig_num equal to the same value of 5.
#
# Return value
#
#   0 on success, -1 on error.

comedi_internal_trigger = _grab("comedi_internal_trigger")
comedi_internal_trigger.restype = c_int                                         #   int comedi_internal_trigger(
comedi_internal_trigger.argtypes = [ POINTER(comedi_t),                         #       comedi_t * device,
                                     c_uint,                                    #       unsigned int subdevice,
                                     c_uint ]                                   #       unsigned int trig_num);


##############################################################################
# comedi_lock — subdevice reservation
#
#   #include <comedilib.h>
#
#   int comedi_lock(	comedi_t * device,
#       unsigned int subdevice);
#
# Description
#
#   The function comedi_lock reserves a subdevice for use by the current 
#   process. While the lock is held, no other process is allowed to read, 
#   write, or configure that subdevice, although other processes can read 
#   information about the subdevice. The lock is released by comedi_unlock, 
#   or when comedi_close is called on device.
#
# Return value
#
#   If successful, 0 is returned. If there is an error, -1 is returned.

comedi_lock = _grab("comedi_lock")
comedi_lock.restype = c_int                                                     #   int comedi_lock(
comedi_lock.argtypes = [ POINTER(comedi_t),                                     #       comedi_t * device,
                         c_uint ]                                               #       unsigned int subdevice);


##############################################################################
# comedi_maxdata_is_chan_specific — maximum sample depends on channel
#
#   #include <comedilib.h>
#
#   int comedi_maxdata_is_chan_specific(	comedi_t * device,
#       unsigned int subdevice);
#
# Description
#
#   If each channel of the specified subdevice may have different maximum 
#   sample values, this function returns 1. Otherwise, this function returns 0. 
#   On error, this function returns -1.

comedi_maxdata_is_chan_specific = _grab("comedi_maxdata_is_chan_specific")
comedi_maxdata_is_chan_specific.restype = c_int                                 #   int comedi_maxdata_is_chan_specific(
comedi_maxdata_is_chan_specific.argtypes = [ POINTER(comedi_t),                 #       comedi_t * device,
                                             c_uint ]                           #       unsigned int subdevice);

##############################################################################
# comedi_open — open a Comedi device
#
#   #include <comedilib.h>
#
#   comedi_t * comedi_open(	const char * filename);
#
# Description
#
#   Open a Comedi device specified by the file filename.
#
# Return value
#
#   If successful, comedi_open returns a pointer to a valid comedi_t structure. 
#   This structure is opaque; the pointer should not be dereferenced by the 
#   application. NULL is returned on failure.

comedi_open = _grab("comedi_open")
comedi_open.restype = POINTER(comedi_t)                                         #   comedi_t * comedi_open(
comedi_open.argtypes = [ c_char_p]                                              #       const char * filename);


##############################################################################
# comedi_range_is_chan_specific — range information depends on channel
#
#   #include <comedilib.h>
#
#   int comedi_range_is_chan_specific(	comedi_t * device,
#       unsigned int subdevice);
#
# Description
#
#   If each channel of the specified subdevice may have different range 
#   information, this function returns 1. Otherwise, this function returns 0. 
#   On error, this function returns -1.

comedi_range_is_chan_specific = _grab("comedi_range_is_chan_specific")
comedi_range_is_chan_specific.restype = c_int                                   #   int comedi_range_is_chan_specific(
comedi_range_is_chan_specific.argtypes = [ POINTER(comedi_t),                   #       comedi_t * device,
                                           c_uint ]                             #       unsigned int subdevice);



##############################################################################
# comedi_set_global_oor_behavior — out-of-range behavior
#
#   #include <comedilib.h>
#
#   enum comedi_oor_behavior comedi_set_global_oor_behavior(	enum comedi_oor_behavior behavior);
# 
# Description
#
#   This function changes the Comedilib out-of-range behavior. This currently 
#   affects the behavior of comedi_to_phys when converting endpoint sample 
#   values, that is, sample values equal to 0 or maxdata. If the out-of-range 
#   behavior is set to COMEDI_OOR_NAN, endpoint values are converted to NAN. 
#   If the out-of-range behavior is set to COMEDI_OOR_NUMBER, the endpoint 
#   values are converted similarly to other values.
#
# Return value
#
#   The previous out-of-range behavior is returned.

comedi_set_global_oor_behavior = _grab("comedi_set_global_oor_behavior")
comedi_set_global_oor_behavior.restype = comedi_oor_behavior                    #   enum comedi_oor_behavior comedi_set_global_oor_behavior(
comedi_set_global_oor_behavior.argtypes = [ comedi_oor_behavior ]               #       enum comedi_oor_behavior behavior);


##############################################################################
# comedi_to_phys — convert sample to physical units
#
#   #include <comedilib.h>
#
#   double comedi_to_phys(	lsampl_t data,
#       comedi_range * range,
#       lsampl_t maxdata);
#
# Description
#
#   Converts parameter data given in sample values (lsampl_t, between 0 and 
#   maxdata) into physical units (double). The parameter range represents the 
#   conversion information to use, and the parameter maxdata represents the 
#   maximum possible data value for the channel that the data was read. The 
#   mapping between physical units is linear and assumes ideal converter 
#   characteristics.
#
#   Conversion of endpoint sample values, that is, sample values equal to 0 or 
#   maxdata, is affected by the Comedilib out-of-range behavior (see function 
#   comedi_set_global_oor_behavior>). If the out-of-range behavior is set to 
#   COMEDI_OOR_NAN, endpoint values are converted to NAN. If the out-of-range 
#   behavior is set to COMEDI_OOR_NUMBER, the endpoint values are converted 
#   similarly to other values.
#
#   If there is an error, NAN is returned.

comedi_to_phys = _grab("comedi_to_phys")
comedi_to_phys.restype = c_double                                               #   double comedi_to_phys(
comedi_to_phys.argtypes = [ lsampl_t,                                           #       lsampl_t data,
                            POINTER(comedi_range),                              #       comedi_range * range,
                            lsampl_t ]                                          #       lsampl_t maxdata);


##############################################################################
# comedi_to_physical — convert sample to physical units using polynomials
#
#   #include <comedilib.h>
#
#   double comedi_to_physical(	lsampl_t data,
#       const comedi_polynomial_t * conversion_polynomial);
#
# Description
#
#   Converts data given in Comedi's integer sample values (lsampl_t, between 
#   0 and maxdata) into physical units (double). The conversion_polynomial 
#   parameter is obtained from either comedi_get_hardcal_converter or 
#   comedi_get_softcal_converter. No range checking of the input data is 
#   performed. It is up to you to check for data values of 0 or maxdata if you 
#   want to detect possibly out-of-range readings.
#
# Return value
#
#   Physical value corresponding to the input sample value.

comedi_to_physical = _grab("comedi_to_physical")
comedi_to_physical.restype = c_double                                           #   double comedi_to_physical(
comedi_to_physical.argtypes = [ lsampl_t,                                       #       lsampl_t data,
                                POINTER(comedi_polynomial_t) ]                  #       const comedi_polynomial_t * conversion_polynomial);





##############################################################################
# comedi_unlock — subdevice reservation
#
#   #include <comedilib.h>
#
#   int comedi_unlock(	comedi_t * device,
#       unsigned int subdevice);
#
# Description
#
#   The function comedi_unlock releases a subdevice locked by comedi_lock.
#
# Return value
#
#       0 on success, otherwise -1.

comedi_unlock = _grab("comedi_unlock")
comedi_unlock.restype = c_int                                                   #   int comedi_unlock(
comedi_unlock.argtypes = [ POINTER(comedi_t),                                   #       comedi_t * device,
                           c_uint ]                                             #       unsigned int subdevice);




##############################################################################
#                   - Begin ASYNCHRONOUS COMMANDS section -
##############################################################################



##############################################################################
# comedi_cancel — stop streaming input/output in progress
#
#   #include <comedilib.h>
#
#   int comedi_cancel(	comedi_t * device,
#       unsigned int subdevice);
#
# Description
#
#   The function comedi_cancel can be used to stop a command previously 
#   started by comedi_command which is still in progress on the subdevice 
#   indicated by the parameters device and subdevice.
#
# Return value
#
#   If successful, 0 is returned, otherwise -1.

comedi_cancel = _grab("comedi_cancel")
comedi_cancel.restype = c_int                                                   #   int comedi_cancel(
comedi_cancel.argtypes = [ POINTER(comedi_t),                                   #       comedi_t * device,
                          c_uint ]                                              #       unsigned int subdevice);


##############################################################################
# comedi_command — start streaming input/output
#
#   #include <comedilib.h>
#
#   int comedi_command(	comedi_t * device,
#       comedi_cmd * command);
#
# Description
#
#   The function comedi_command starts a streaming input or output. The 
#   command structure pointed to by command specifies settings for the 
#   acquisition. The command must be able to pass comedi_command_test with a 
#   return value of 0, or comedi_command will fail. For input subdevices, 
#   sample values are read using the function read on the device file. For 
#   output subdevices, sample values are written using the function write.
#
# Return value
#
#   If successful, 0 is returned, otherwise -1.


comedi_command = _grab("comedi_command")
comedi_command.restype = c_int                                                  #   int comedi_command(
comedi_command.argtypes = [ POINTER(comedi_t),                                  #       comedi_t * device,
                            POINTER(comedi_cmd) ]                               #       comedi_cmd * command);



##############################################################################
# comedi_command_test — test streaming input/output configuration
#
#   #include <comedilib.h>
#
#   int comedi_command_test(	comedi_t * device,
#       comedi_cmd * command);
#
# Description
#
#   The function comedi_command_test tests the command structure pointed to by 
#   the parameter command and returns an integer describing the testing stages 
#   that were successfully passed. In addition, if elements of the comedi_cmd 
#   structure are invalid, they may be modified. Source elements are modified 
#   to remove invalid source triggers. Argument elements are adjusted or 
#   rounded to the nearest valid value.
#
#   The meanings of the return value are as follows:
#
#       0 indicates a valid command.
#
#       1 indicates that one of the …_src members of the command contained an 
#       unsupported trigger. The bits corresponding to the unsupported triggers 
#       are zeroed.
#
#       2 indicates that the particular combination of …_src settings is not 
#       supported by the driver, or that one of the …_src members has the bit 
#       corresponding to multiple trigger sources set at the same time.
#
#       3 indicates that one of the …_arg members of the command is set outside 
#       the range of allowable values. For instance, an argument for a 
#       TRIG_TIMER source which exceeds the board's maximum speed. The invalid
#        …_arg members will be adjusted to valid values.
#
#       4 indicates that one of the …_arg members required adjustment. For 
#       instance, the argument of a TRIG_TIMER source may have been rounded to 
#       the nearest timing period supported by the board.
#
#       5 indicates that some aspect of the command's chanlist is unsupported 
#       by the board. For example, some analog input boards require that all 
#       channels in the chanlist use the same input range.


comedi_command_test = _grab("comedi_command_test")
comedi_command_test.restype = c_int                                             #   int comedi_command_test(
comedi_command_test.argtypes = [ POINTER(comedi_t),                             #       comedi_t * device,
                                 POINTER(comedi_cmd) ]                          #       comedi_cmd * command);



##############################################################################
# comedi_get_buffer_contents — streaming buffer status
#
#   #include <comedilib.h>
#
#   int comedi_get_buffer_contents(	comedi_t * device,
#       unsigned int subdevice);
#
# Description
#
#   The function comedi_get_buffer_contents is used on a subdevice that has a 
#   Comedi command in progress. The number of bytes that are available in the 
#   streaming buffer is returned. If there is an error, -1 is returned.

comedi_get_buffer_contents = _grab("comedi_get_buffer_contents")
comedi_get_buffer_contents.restype = c_int                                      #   int comedi_get_buffer_contents(
comedi_get_buffer_contents.argtypes = [ POINTER(comedi_t),                      #       comedi_t * device,
                                        c_uint ]                                #       unsigned int subdevice);

##############################################################################
# comedi_get_buffer_offset — streaming buffer status
#
#   #include <comedilib.h>
#
#   int comedi_get_buffer_offset(	comedi_t * device,
#       unsigned int subdevice);
#
# Description
#
#   The function comedi_get_buffer_offset is used on a subdevice that has a 
#   Comedi command in progress. This function returns the offset in bytes of 
#   the read pointer in the streaming buffer. This offset is only useful for 
#   memory mapped buffers. If there is an error, -1 is returned.


comedi_get_buffer_offset = _grab("comedi_get_buffer_offset")
comedi_get_buffer_offset.restype = c_int                                        #   int comedi_get_buffer_offset(
comedi_get_buffer_offset.argtypes = [ POINTER(comedi_t),                        #       comedi_t * device,
                                      c_uint ]                                  #       unsigned int subdevice);



##############################################################################
# comedi_get_buffer_size — streaming buffer size of subdevice
#
#   #include <comedilib.h>
#
#   int comedi_get_buffer_size(	comedi_t * device,
#       unsigned int subdevice);
#
# Description
#
#   The function comedi_get_buffer_size returns the size (in bytes) of the 
#   streaming buffer for the subdevice specified by device and subdevice. 
#   On error, -1 is returned.


comedi_get_buffer_size = _grab("comedi_get_buffer_size")
comedi_get_buffer_size.restype = c_int                                          #   int comedi_get_buffer_size(
comedi_get_buffer_size.argtypes = [ POINTER(comedi_t),                          #       comedi_t * device,
                                    c_uint ]                                    #       unsigned int subdevice);


##############################################################################
# comedi_get_cmd_generic_timed — streaming input/output capabilities
#
#   #include <comedilib.h>
#
#   int comedi_get_cmd_generic_timed(	comedi_t * device,
#       unsigned int subdevice,
#       comedi_cmd * command,
#       unsigned int chanlist_len,
#       unsigned int scan_period_ns);
#
# Description
#
#   The command capabilities of the subdevice indicated by the parameters 
#   device and subdevice are probed, and the results placed in the command 
#   structure pointed to by the parameter command. The command structure 
#   pointed to by command is modified to be a valid command that can be used 
#   as a parameter to comedi_command (after the command has additionally been 
#   assigned a valid chanlist array). The command measures scans consisting 
#   of chanlist_len channels at a scan rate that corresponds to a period of 
#   scan_period_ns nanoseconds. The rate is adjusted to a rate that the 
#   device can handle.
#
# Return value
#
#   If successful, 0 is returned, otherwise -1.

comedi_get_cmd_generic_timed = _grab("comedi_get_cmd_generic_timed")
comedi_get_cmd_generic_timed.restype = c_int                                    #   int comedi_get_cmd_generic_timed(
comedi_get_cmd_generic_timed.argtypes = [ POINTER(comedi_t),                    #       comedi_t * device,
                                          c_uint,                               #       unsigned int subdevice,
                                          POINTER(comedi_cmd),                  #       comedi_cmd * command,
                                          c_uint,                               #       unsigned int chanlist_len,
                                          c_uint ]                              #       unsigned int scan_period_ns);

##############################################################################
# comedi_get_cmd_src_mask — streaming input/output capabilities
#
#   #include <comedilib.h>
#
#   int comedi_get_cmd_src_mask(	comedi_t * device,
#       unsigned int subdevice,
#       comedi_cmd * command);
#
# Description
#
#   The command capabilities of the subdevice indicated by the parameters 
#   device and subdevice are probed, and the results placed in the command 
#   structure pointed to by command. The trigger source elements of the 
#   command structure are set to be the bitwise-or of the subdevice's 
#   supported trigger sources. Other elements in the structure are undefined.
#
# Return value
#
#   If successful, 0 is returned, otherwise -1.

comedi_get_cmd_src_mask = _grab("comedi_get_cmd_src_mask")
comedi_get_cmd_src_mask.restype = c_int                                         #   int comedi_get_cmd_src_mask(
comedi_get_cmd_src_mask.argtypes= [ POINTER(comedi_t),                          #       comedi_t * device,
                                    c_uint,                                     #       unsigned int subdevice,
                                    POINTER(comedi_cmd) ]                       #       comedi_cmd * command);


##############################################################################
# comedi_get_max_buffer_size — maximum streaming buffer size
#
#   #include <comedilib.h>
#
#   int comedi_get_max_buffer_size(	comedi_t * device,
#       unsigned int subdevice);
#
# Description
#
#   The function comedi_get_max_buffer_size returns the maximum allowable size 
#   (in bytes) of the streaming buffer for the subdevice specified by device 
#   and subdevice. Changing the maximum buffer size can be accomplished with 
#   comedi_set_max_buffer_size or with the comedi_config program, and requires 
#   appropriate privileges. On error, -1 is returned.

comedi_get_max_buffer_size = _grab("comedi_get_max_buffer_size")
comedi_get_max_buffer_size.restype = c_int                                      #   int comedi_get_max_buffer_size(
comedi_get_max_buffer_size.argtypes = [ POINTER(comedi_t),                      #       comedi_t * device,
                                        c_uint ]                                #       unsigned int subdevice);


##############################################################################
# comedi_get_read_subdevice — find streaming input subdevice
#
#   #include <comedilib.h>
#
#   int comedi_get_read_subdevice(	comedi_t * device);
#
# Description
#
#   The function comedi_get_read_subdevice returns the index of the subdevice 
#   whose streaming input buffer is accessible through the device device. If 
#   there is no such subdevice, -1 is returned.

comedi_get_read_subdevice = _grab("comedi_get_read_subdevice")
comedi_get_read_subdevice.restype = c_int                                       #   int comedi_get_read_subdevice(
comedi_get_read_subdevice.argyptes = [ POINTER(comedi_t) ]                      #       comedi_t * device);


##############################################################################
# comedi_get_write_subdevice — find streaming output subdevice
#
#   #include <comedilib.h>
#
#   int comedi_get_write_subdevice(	comedi_t * device);
#
# Description
#
#   The function comedi_get_write_subdevice returns the index of the subdevice 
#   whose streaming output buffer is accessible through the device device. If 
#   there is no such subdevice, -1 is returned.

comedi_get_write_subdevice = _grab("comedi_get_write_subdevice")
comedi_get_write_subdevice.restype = c_int                                      #   int comedi_get_write_subdevice(
comedi_get_write_subdevice.argtypes = [ POINTER(comedi_t) ]                     #       comedi_t * devi

##############################################################################
# comedi_mark_buffer_read — streaming buffer control
#
#   #include <comedilib.h>
#
#   int comedi_mark_buffer_read(	comedi_t * device,
#       unsigned int subdevice,
#       unsigned int num_bytes);
#
# Description
#
#   The function comedi_mark_buffer_read is used on a subdevice that has a 
#   Comedi input command in progress. It should only be used if you are using 
#   a mmap mapping to read data from Comedi's buffer (as opposed to calling 
#   read on the device file), since Comedi will automatically keep track of 
#   how many bytes have been transferred via read calls. This function is used 
#   to indicate that the next num_bytes bytes in the buffer are no longer 
#   needed and may be discarded.
#
# Return value
#
#   The function comedi_mark_buffer_read returns the number of bytes 
#   successfully marked as read, or -1 on error. The return value may be less 
#   than num_bytes if you attempt to mark more bytes read than are currently 
#   available for reading, or if num_bytes must be rounded down to be an exact 
#   multiple of the subdevice's sample size (either sizeof(sampl_t) or 
#   sizeof(lsampl_t)).


comedi_mark_buffer_read = _grab("comedi_mark_buffer_read")
comedi_mark_buffer_read.restype = c_int                                         #   int comedi_mark_buffer_read(
comedi_mark_buffer_read.argtypes = [ POINTER(comedi_t),                         #       comedi_t * device,
                                     c_uint,                                    #       unsigned int subdevice,
                                     c_uint ]                                   #       unsigned int num_bytes);



##############################################################################
# comedi_mark_buffer_written — streaming buffer control
#
#   #include <comedilib.h>
#
#   int comedi_mark_buffer_written(	comedi_t * device,
#       unsigned int subdevice,
#       unsigned int num_bytes);
#
# Description
#
#       The function comedi_mark_buffer_written is used on a subdevice that 
#       has a Comedi output command in progress. It should only be used if you 
#       are using a mmap mapping to write data to Comedi's buffer (as opposed 
#       to calling write on the device file), since Comedi will automatically 
#       keep track of how many bytes have been transferred via write calls. 
#       This function is used to indicate that the next num_bytes bytes in the 
#       buffer are valid and may be sent to the device.
#
# Return value
#
#   The function comedi_mark_buffer_written returns number of bytes 
#   successfully marked as written, or -1 on error. The return value may be 
#   less than num_bytes if you attempt to mark more bytes written than the 
#   amount of free space currently available in the output buffer, or if 
#   num_bytes must be rounded down to be an exact multiple of the subdevice's 
#   sample size (either sizeof(sampl_t) or sizeof(lsampl_t)).

comedi_mark_buffer_written = _grab("comedi_mark_buffer_written")
comedi_mark_buffer_written.restype = c_int                                      #   int comedi_mark_buffer_written(
comedi_mark_buffer_written.argtypes = [ POINTER(comedi_t),                      #       comedi_t * device,
                                        c_uint,                                 #       unsigned int subdevice,
                                        c_uint ]                                #       unsigned int num_bytes);




##############################################################################
# comedi_poll — force updating of streaming buffer
#
#   #include <comedilib.h>
#
#   int comedi_poll(	comedi_t * device,
#       unsigned int subdevice);
#
# Description
#
#   The function comedi_poll is used on a subdevice that has a Comedi command 
#   in progress in order to update the streaming buffer. If supported by the 
#   driver, all available samples are copied to the streaming buffer. These 
#   samples may be pending in DMA buffers or device FIFOs. If successful, the 
#   number of additional bytes available is returned. If there is an error, 
#   -1 is returned.

comedi_poll = _grab("comedi_poll")
comedi_poll.restype = c_int                                                     #   int comedi_poll(
comedi_poll.argtypes = [ POINTER(comedi_t),                                     #       comedi_t * device,
                         c_uint ]                                               #       unsigned int subdevice);



##############################################################################
# comedi_set_buffer_size — streaming buffer size of subdevice
#
#   #include <comedilib.h>
#
#   int comedi_set_buffer_size(	comedi_t * device,
#       unsigned int subdevice,
#       unsigned int size);
#
# Description
#
#   The function comedi_set_buffer_size changes the size of the streaming 
#   buffer for the subdevice specified by device and subdevice. The buffer 
#   size will be set to size bytes, rounded up to a multiple of the virtual 
#   memory page size. The virtual memory page size can be determined using 
#   sysconf(_SC_PAGE_SIZE).
#
#   This function does not require special privileges. However, it is limited 
#   to a (adjustable) maximum buffer size, which can be changed by a privileged 
#   user calling comedi_set_max_buffer_size, or running the program comedi_config.
#
# Return value
#
#   The new buffer size in bytes is returned on success. On error, -1 is returned.

comedi_set_buffer_size = _grab("comedi_set_buffer_size")
comedi_set_buffer_size.restype = c_int                                          #   int comedi_set_buffer_size(
comedi_set_buffer_size.argtypes = [ POINTER(comedi_t),                          #       comedi_t * device,
                                    c_uint,                                     #       unsigned int subdevice,
                                    c_uint ]                                    #       unsigned int size);


##############################################################################
# comedi_set_max_buffer_size — streaming maximum buffer size of subdevice
#
#   #include <comedilib.h>
#
#   int comedi_set_max_buffer_size(	comedi_t * device,
#       unsigned int subdevice,
#       unsigned int max_size);
#
# Description
#
#   The function comedi_set_max_buffer_size changes the maximum allowable 
#   size (in bytes) of the streaming buffer for the subdevice specified by 
#   device and subdevice. Changing the maximum buffer size requires the user 
#   to have appropriate privileges.
#
# Return value
#
#   The new maximum buffer size is returned on success. On error, -1 is returned.

comedi_set_max_buffer_size = _grab("comedi_set_max_buffer_size")
comedi_set_max_buffer_size.restype = c_int                                      #   int comedi_set_max_buffer_size(
comedi_set_max_buffer_size.argtypes = [ POINTER(comedi_t),                      #       comedi_t * device,
                                        c_uint,                                 #       unsigned int subdevice,
                                        c_uint ]                                #       unsigned int max_siz



##############################################################################
#                   - Begin CALIBRATION COMMANDS section -
##############################################################################



##############################################################################
# comedi_apply_calibration — set hardware calibration from file
#
#   #include <comedilib.h>
#
#   int comedi_apply_calibration(	comedi_t * device,
#       unsigned int subdevice,
#       unsigned int channel,
#       unsigned int range,
#       unsigned int aref,
#       const char * file_path);
#
# Description
#
#   The function comedi_apply_calibration sets the hardware calibration for 
#   the subdevice specified by device and subdevice so that it is in proper 
#   calibration when using the channel specified by channel, range index 
#   specified by range and analog reference specified by aref. It does so by 
#   performing writes to the appropriate channels of the board's calibration 
#   subdevice(s). Depending on the hardware, the calibration settings used may 
#   or may not depend on the channel, range, or analog reference. Furthermore, 
#   the calibrations appropriate for different channel, range, and analog 
#   reference parameters may not be able to be applied simultaneously. For 
#   example, some boards cannot have their analog inputs calibrated for more 
#   than one input range simultaneously. Applying a calibration for range 1 
#   may blow away a previously applied calibration for range 0. Or, applying 
#   a calibration for analog input channel 0 may cause the same calibration 
#   to be applied to all the other analog input channels as well. Your only 
#   guarantee is that calls to comedi_apply_calibration on different subdevices 
#   will not interfere with each other.
#
#   In practice, their are some rules of thumb on how calibrations behave. 
#   No calibrations depend on the analog reference. A multiplexed analog input 
#   will have calibration settings that do not depend on the channel, and 
#   applying a setting for one channel will affect all channels equally. 
#   Analog outputs, and analog inputs with independent a/d converters for each 
#   input channel, will have calibration settings which do depend on the 
#   channel, and the settings for each channel will be independent of the other 
#   channels.
#
#   If you wish to investigate exactly what comedi_apply_calibration is doing, 
#   you can perform reads on your board's calibration subdevice to see which 
#   calibration channels it is changing. You can also try to decipher the 
#   calibration file directly (it's a text file).
#
#   The file_path parameter can be used to specify the file which contains the 
#   calibration information. If file_path is NULL, then Comedilib will use a 
#   default file location. The calibration information used by this function 
#   is generated by the comedi_calibrate program (see its man page).
#
#   The functions comedi_parse_calibration_file, 
#   comedi_apply_parsed_calibration, and comedi_cleanup_calibration_file 
#   provide the same functionality at a slightly lower level.
#
# Return value
#
#   Returns 0 on success, -1 on failure. 


comedi_apply_calibration = _grab("comedi_apply_calibration")
comedi_apply_calibration.restype = c_int                                        #   int comedi_apply_calibration(
comedi_apply_calibration.argtypes = [ POINTER(comedi_t),                        #       comedi_t * device,
                                      c_uint,                                   #       unsigned int subdevice,
                                      c_uint,                                   #       unsigned int channel,
                                      c_uint,                                   #       unsigned int range,
                                      c_uint,                                   #       unsigned int aref,
                                      c_char_p ]                                #       const char * file_path);

##############################################################################
# comedi_apply_parsed_calibration — set calibration from memory
#
#   #include <comedilib.h>
#
#   int comedi_apply_parsed_calibration(	comedi_t * device,
#       unsigned int subdevice,
#       unsigned int channel,
#       unsigned int range,
#       unsigned int aref,
#       const comedi_calibration_t * calibration);
#
# Description
#
#   This function is similar to comedi_apply_calibration, except the 
#   calibration information is read from memory instead of a file. This 
#   function can be more efficient than comedi_apply_calibration since the 
#   calibration file does not need to be reparsed with every call. The value 
#   of parameter calibration is obtained by a call to comedi_parse_calibration_file.
#
# Return value
#
#   Returns 0 on success, -1 on failure. 

comedi_apply_parsed_calibration = _grab("comedi_apply_parsed_calibration")
comedi_apply_parsed_calibration.restype = c_int                                 #   int comedi_apply_parsed_calibration(
comedi_apply_parsed_calibration.argtypes = [ POINTER(comedi_t),                 #       comedi_t * device,
                                             c_uint,                            #       unsigned int subdevice,
                                             c_uint,                            #       unsigned int channel,
                                             c_uint,                            #       unsigned int range,
                                             c_uint,                            #       unsigned int aref,
                                             POINTER(comedi_calibration_t)]     #       const comedi_calibration_t * calibration);




##############################################################################
# comedi_cleanup_calibration — free calibration resources
#
#   #include <comedilib.h>
#
#   void comedi_cleanup_calibration(	comedi_calibration_t * calibration);
#
# Description
#
#   This function frees the resources associated with a comedi_calibration_t 
#   obtained from comedi_parse_calibration_file. The comedi_calibration_t pointed 
#   to by calibration can not be used again after calling this function. 

comedi_cleanup_calibration = _grab("comedi_cleanup_calibration")
comedi_cleanup_calibration.restype = c_void                                     #   void comedi_cleanup_calibration(
comedi_cleanup_calibration.argtypes = [ POINTER(comedi_calibration_t) ]         #       comedi_calibration_t * calibration);


##############################################################################
# comedi_get_default_calibration_path — get default calibration file path
#
#   #include <comedilib.h>
#
#   char * comedi_get_default_calibration_path(	comedi_t * device);
#
# Description
#
#   This function returns a pointer to a string containing a default 
#   calibration file path appropriate for the Comedi device specified by 
#   device. Memory for the string is allocated by the function, and should be 
#   freed with the C library function free when the string is no longer needed.
#
# Return value
#
#   A string which contains a file path useable by comedi_parse_calibration_file. 
#   On error, NULL is returned. 

comedi_get_default_calibration_path = _grab("comedi_get_default_calibration_path") 
comedi_get_default_calibration_path.restype = c_char_p                          #    char * comedi_get_default_calibration_path(
comedi_get_default_calibration_path.argtypes = [ POINTER(comedi_t) ]            #       comedi_t * device);



##############################################################################
# comedi_get_hardcal_converter — get converter for hardware-calibrated subdevice
#
#   #include <comedilib.h>
#
#   int comedi_get_hardcal_converter(	comedi_t * device,
#       unsigned subdevice,
#       unsigned channel,
#       unsigned range,
#       enum comedi_conversion_direction direction,
#       comedi_polynomial_t * converter);
#
# Description
#
#   The function comedi_get_hardcal_converter initializes the comedi_polynomial_t 
#   pointed to by converter so it can be passed to either comedi_to_physical, 
#   or comedi_from_physical. The result can be used to convert data from the 
#   specified subdevice, channel, and range. The direction parameter specifies 
#   whether converter will be passed to comedi_to_physical or comedi_from_physical.
#
#   This function initializes the comedi_polynomial_t pointed to by converter 
#   as a simple linear function with no calibration information, appropriate 
#   for boards which do their gain/offset/nonlinearity corrections in hardware. 
#   If your board needs calibration to be performed in software by the host 
#   computer, use comedi_get_softcal_converter instead. A subdevice will 
#   advertise the fact that it depends on a software calibration with the 
#   SDF_SOFT_CALIBRATED subdevice flag.
#
#   The result of this function will only depend on the channel parameter if 
#   either comedi_range_is_chan_specific or comedi_maxdata_is_chan_specific 
#   returns true for the specified subdevice.
#
# Return value
#
#   Returns 0 on success, -1 on failure. 

comedi_get_hardcal_converter = _grab("comedi_get_hardcal_converter")
comedi_get_hardcal_converter.restype = c_int                                    #   int comedi_get_hardcal_converter(
comedi_get_hardcal_converter.argtypes = [ POINTER(comedi_t),                    #       comedi_t * device,
                                          c_uint,                               #       unsigned subdevice,
                                          c_uint,                               #       unsigned channel,
                                          c_uint,                               #       unsigned range,
                                          comedi_conversion_direction,          #       enum comedi_conversion_direction direction,
                                          POINTER(comedi_polynomial_t) ]        #       comedi_polynomial_t * converter);


##############################################################################
# comedi_get_softcal_converter — get converter for software-calibrated subdevice
#
#   #include <comedilib.h>
#
#   int comedi_get_softcal_converter(	unsigned subdevice,
#       unsigned channel,
#       unsigned range,
#       enum comedi_conversion_direction direction,
#       const comedi_calibration_t * parsed_calibration,
#       comedi_polynomial_t * converter);
#
# Description
#
#   The function comedi_get_softcal_converter initializes the comedi_polynomial_t 
#   pointed to by converter so it can be passed to either comedi_to_physical or 
#   comedi_from_physical. The comedi_polynomial_t pointed to by converter can 
#   then be used to convert data for the specified subdevice, channel, and 
#   range. The direction parameter specifies whether converter will be passed 
#   to comedi_to_physical or comedi_from_physical. The parsed_calibration 
#   parameter points to the software calibration values for your device, and 
#   may be obtained by calling comedi_parse_calibration_file on a calibration 
#   file generated by the comedi_soft_calibrate program.
#
#   This function is only useful for boards that perform their calibrations in 
#   software on the host computer. A subdevice will advertise the fact that it 
#   depends on a software calibration with the SDF_SOFT_CALIBRATED subdevice 
#   flag.
#
#   Whether or not the result of this function actually depends on the channel 
#   parameter is hardware dependent. For example, the calibration of a 
#   multiplexed analog input will typically not depend on the channel, only the 
#   range. Analog outputs will typically use different calibrations for each 
#   output channel.
#
#   Software calibrations are implemented as polynomials (up to third order). 
#   Since the inverse of a polynomial of order higher than one can't be 
#   represented exactly as another polynomial, you may not be able to get 
#   converters for the “reverse” direction. For example, you may be able to 
#   get a converter for an analog input in the COMEDI_TO_PHYSICAL direction, 
#   but not in the COMEDI_FROM_PHYSICAL direction.
#
# Return value
#
#   Returns 0 on success, -1 on failure. 

comedi_get_softcal_converter = _grab("comedi_get_softcal_converter")
comedi_get_softcal_converter.restype = c_int                                    #   int comedi_get_softcal_converter(
comedi_get_softcal_converter.argtypes = [ c_uint,                               #       unsigned subdevice,
                                          c_uint,                               #       unsigned channel,
                                          c_uint,                               #       unsigned range,
                                          comedi_conversion_direction,         #       enum comedi_conversion_direction direction,
                                          POINTER(comedi_calibration_t),        #       const comedi_calibration_t * parsed_calibration,
                                          POINTER(comedi_polynomial_t) ]        #       comedi_polynomial_t * converter);



##############################################################################
# comedi_parse_calibration_file — load contents of calibration file
#
#   #include <comedilib.h>
#
#   comedi_calibration_t * comedi_parse_calibration_file(	const char * file_path);
#
# Description
#
#   This function parses a calibration file (produced by the comedi_calibrate 
#   or comedi_soft_calibrate programs) and returns a pointer to a 
#   comedi_calibration_t which can be passed to the comedi_apply_parsed_calibration 
#   or comedi_get_softcal_converter functions. When you are finished using the 
#   comedi_calibration_t, you should call comedi_cleanup_calibration to free 
#   the resources associated with the comedi_calibration_t.
#
#   The comedi_get_default_calibration_path function may be useful in 
#   conjunction with this function.
#
# Return value
#
#   A pointer to parsed calibration information on success, or NULL on failure. 

comedi_parse_calibration_file = _grab("comedi_parse_calibration_file")          
comedi_parse_calibration_file.restype = POINTER(comedi_calibration_t)           #   comedi_calibration_t * comedi_parse_calibration_file(
comedi_parse_calibration_file.argtypes = [ c_char_p ]                           #       const char * file_path);





##############################################################################
#                   - Begin DIGITAL I/O section -
##############################################################################


##############################################################################
# comedi_dio_bitfield2 — read/write multiple digital channels
#
#   #include <comedilib.h>
#
#   int comedi_dio_bitfield2(	comedi_t * device,
#       unsigned int subdevice,
#       unsigned int write_mask,
#       unsigned int * bits,
#       unsigned int base_channel);
#
# Description
#
#   The function comedi_dio_bitfield2 allows multiple channels to be read or 
#   written together on a digital input, output, or configurable digital I/O 
#   device. The parameter write_mask and the value pointed to by bits are 
#   interpreted as bit fields, with the least significant bit representing 
#   channel base_channel. For each bit in write_mask that is set to 1, the 
#   corresponding bit in *bits is written to the digital output channel. After 
#   writing all the output channels, each channel is read, and the result 
#   placed in the approprate bits in *bits. The result of reading an output 
#   channel is the last value written to the output channel.
#
#   All the channels might not be read or written at the exact same time. For 
#   example, the driver may need to sequentially write to several registers in 
#   order to set all the digital channels specified by the write_mask and 
#   base_channel parameters.
#
# Return value
#
#   If successful, 0 is returned, otherwise -1. 

comedi_dio_bitfield2 = _grab("comedi_dio_bitfield2")
comedi_dio_bitfield2.restype = c_int                                            #   int comedi_dio_bitfield2(
comedi_dio_bitfield2.argtypes = [ POINTER(comedi_t),                            #       comedi_t * device,
                                  c_uint,                                       #       unsigned int subdevice,
                                  c_uint,                                       #       unsigned int write_mask,
                                  POINTER(c_uint),                              #       unsigned int * bits,
                                  c_uint ]                                      #       unsigned int base_channel);


##############################################################################
# comedi_dio_config — change input/output properties of channel
#
#   #include <comedilib.h>
#
#   int comedi_dio_config(	comedi_t * device,
#       unsigned int subdevice,
#       unsigned int channel,
#       unsigned int direction);
#
# Description
#
#   The function comedi_dio_config configures individual channels in a digital 
#   I/O subdevice to be either input or output, depending on the value of 
#   direction. Valid directions are COMEDI_INPUT or COMEDI_OUTPUT.
#
#   Depending on the characteristics of the hardware device, multiple channels 
#   might be grouped together in hardware when configuring the input/output 
#   direction. In this case, a single call to comedi_dio_config for any channel 
#   in the group will affect the entire group.
#
# Return value
#
#   If successful, 0 is returned, otherwise -1. 

comedi_dio_config = _grab("comedi_dio_config")
comedi_dio_config.restype = c_int                                               #   int comedi_dio_config(
comedi_dio_config.argtypes = [ POINTER(comedi_t),                               #       comedi_t * device,
                               c_uint,                                          #       unsigned int subdevice,
                               c_uint,                                          #       unsigned int channel,
                               c_uint ]                                         #       unsigned int direction);


##############################################################################
# comedi_dio_get_config — query input/output properties of channel
#
#   #include <comedilib.h>
#
#   int comedi_dio_get_config(	comedi_t * device,
#       unsigned int subdevice,
#       unsigned int channel,
#       unsigned int * direction);
#
# Description
#
#   The function comedi_dio_get_config queries the input/output configuration 
#   of an individual channel in a digital I/O subdevice (see comedi_dio_config). 
#   On success, *direction will be set to either COMEDI_INPUT or COMEDI_OUTPUT.
#
# Return value
#
#   If successful, 0 is returned, otherwise -1.

comedi_dio_get_config = _grab("comedi_dio_get_config")
comedi_dio_get_config.restype = c_int                                           #   int comedi_dio_get_config(
comedi_dio_get_config.argtypes = [ POINTER(comedi_t),                           #       comedi_t * device,
                                   c_uint,                                      #       unsigned int subdevice,
                                   c_uint,                                      #       unsigned int channel,
                                   POINTER(c_uint) ]                            #       unsigned int * direction);


##############################################################################
# comedi_dio_read — read single bit from digital channel
#
#   #include <comedilib.h>
#
#   int comedi_dio_read(	comedi_t * device,
#       unsigned int subdevice,
#       unsigned int channel,
#       unsigned int * bit);
#
# Description
#
#   The function comedi_dio_read reads the channel channel belonging to the 
#   subdevice subdevice of device device. The data value that is read is stored 
#   in the *bit. This function is equivalent to:
#
#   comedi_data_read(device, subdevice, channel, 0, 0, bit);
#
#   This function does not require a digital subdevice or a subdevice with a 
#   maximum data value of 1 to work properly.
#
#   If you wish to read multiple digital channels at once, it is more efficient 
#   to use comedi_dio_bitfield2 than to call this function multiple times.
#
# Return value
#
#   Return values and errors are the same as comedi_data_read. 

comedi_dio_read = _grab("comedi_dio_read")
comedi_dio_read.restype = c_int                                                 #   int comedi_dio_read(
comedi_dio_read.argtypes = [ POINTER(comedi_t),                                 #       comedi_t * device,
                             c_uint,                                            #       unsigned int subdevice,
                             c_uint,                                            #       unsigned int channel,
                             POINTER(c_uint) ]                                  #       unsigned int * bit);



##############################################################################
# comedi_dio_write — write single bit to digital channel
#
#   #include <comedilib.h>
#
#   int comedi_dio_write(	comedi_t * device,
#       unsigned int subdevice,
#       unsigned int channel,
#       unsigned int bit);
#
# Description
#
#   The function writes the value bit to the channel channel belonging to the 
#   subdevice subdevice of device device. This function is equivalent to:
#
#   comedi_data_write(device, subdevice, channel, 0, 0, bit);
#
#   This function does not require a digital subdevice or a subdevice with a 
#   maximum data value of 1 to work properly.
#
#   If you wish to write multiple digital channels at once, it is more efficient 
#   to use comedi_dio_bitfield2 than to call this function multiple times.
#
# Return value
#
#   Return values and errors are the same as comedi_data_write.

comedi_dio_write = _grab("comedi_dio_write")
comedi_dio_write.restype = c_int                                                #   int comedi_dio_write(
comedi_dio_write.argtypes = [ POINTER(comedi_t),                                #       comedi_t * device,
                              c_uint,                                           #       unsigned int subdevice,
                              c_uint,                                           #       unsigned int channel,
                              c_uint ]                                          #       unsigned int bit);




##############################################################################
#                   - Begin ERROR REPORTING section -
##############################################################################


##############################################################################
# comedi_errno — number of last Comedilib error
#
#   #include <comedilib.h>
#
#   int comedi_errno(	void);	 
#
# Description
#
#   When a Comedilib function fails, it usually returns -1 or NULL, depending 
#   on the return type. An internal library variable stores an error number, 
#   which can be retrieved by calling comedi_errno This error number can be 
#   converted to a human-readable form by the functions comedi_perror and 
#   comedi_strerror.
#
#   These functions are intended to mimic the behavior of the standard C 
#   library functions perror, strerror, and errno. In particular, Comedilib 
#   functions sometimes return an error that is generated inside the C library; 
#   the comedi error message in this case is the same as the C library.
#
#   The function comedi_errno returns an integer describing the most recent 
#   Comedilib error. This integer may be used as the errnum parameter for 
#   comedi_strerror.


comedi_errno = _grab("comedi_errno")
comedi_errno.restype = c_int                                                    #   int comedi_errno(
comedi_errno.argtypes = [ c_void ]                                              #       void);	


##############################################################################
# comedi_loglevel — change Comedilib logging properties
#
#   #include <comedilib.h>
#
#   int comedi_loglevel(	int loglevel);
#
# Description
#
#   This function affects the output of debugging and error messages from 
#   Comedilib. By increasing the log level loglevel, additional debugging 
#   information will be printed. Error and debugging messages are printed to 
#   the standard error output stream stderr.
#
#   The default loglevel can be set by using the environment variable 
#   COMEDI_LOGLEVEL. The default log level is 1.
#
#   In order to conserve resources, some debugging information is disabled by 
#   default when Comedilib is compiled.
#
#   The meaning of the log levels is as follows:
#
#   Loglevel    Behavior
#       0       Comedilib prints nothing.
#       1       (default) Comedilib prints error messages when there is a 
#                   self-consistency error (i.e., an internal bug.)
#       2       Comedilib prints an error message when an invalid parameter is 
#                   passed.
#       3       Comedilib prints an error message whenever an error is 
#                   generated in the Comedilib library or in the C library, 
#                   when called by Comedilib.
#       4       Comedilib prints a lot of junk.
#
# Return value
#
#   This function returns the previous log level.

comedi_loglevel = _grab("comedi_loglevel")
comedi_loglevel.restype = c_int                                                 #   int comedi_loglevel(
comedi_loglevel.argtypes = [ c_int ]                                            #       int loglevel);


##############################################################################
# comedi_perror — print a Comedilib error message
#
#   #include <comedilib.h>
#
#   void comedi_perror(	const char * s);
#
# Description
#
#   When a Comedilib function fails, it usually returns -1 or NULL, depending 
#   on the return type. An internal library variable stores an error number, 
#   which can be retrieved with comedi_errno. This error number can be 
#   converted to a human-readable form by the functions comedi_perror or 
#   comedi_strerror.
#
#   These functions are intended to mimic the behavior of the standard C 
#   library functions perror, strerror, and errno. In particular, Comedilib 
#   functions sometimes return an error that is generated inside the C library; 
#   the comedi error message in this case is the same as the C library.
#
#   The function comedi_perror prints an error message to the standard error 
#   output stream stderr. The error message consists of the argument string s, 
#   a colon, a space, a description of the error condition, and a new line.


comedi_perror = _grab("comedi_perror")
comedi_perror.restype = c_int                                                  #   void comedi_perror(
comedi_perror.argtypes = [ c_char_p ]                                           #       const char * s);


##############################################################################
# comedi_strerror — return string describing Comedilib error code
#
#   #include <comedilib.h>
#
#   const char * comedi_strerror(	int errnum);
#
# Description
#
#   When a Comedilib function fails, it usually returns -1 or NULL, depending 
#   on the return type. An internal library variable stores an error number, 
#   which can be retrieved with comedi_errno. This error number can be 
#   converted to a human-readable form by the functions comedi_perror or 
#   comedi_strerror.
#
#   These functions are intended to mimic the behavior of the standard C 
#   library functions perror, strerror, and errno. In particular, Comedilib 
#   functions sometimes return an error that is generated inside the C library; 
#   the comedi error message in this case is the same as the C library.
#
#   The function comedi_strerror returns a pointer to a character string 
#   describing the Comedilib error errnum. The returned string may be modified 
#   by a subsequent call to a strerr or perror function (either the libc or 
#   Comedilib versions). An unrecognized error number will return a pointer to 
#   the string “undefined error”, or similar.


comedi_strerror = _grab("comedi_strerror")
comedi_strerror.restype = c_char_p                                              #   const char * comedi_strerror(
comedi_strerror.argtypes = [ c_int ]                                            #       int errnum);




##############################################################################
#                   - Begin EXTENSIONS section -
##############################################################################


##############################################################################
# comedi_arm — arm a subdevice
#
#   #include <comedilib.h>
#
#   int comedi_arm(	comedi_t * device,
#       unsigned int subdevice,
#       unsigned int source);
#
# Description
#
#   This function arms a subdevice. It may, for example, arm a counter to begin 
#   counting. The source parameter specifies what source should trigger the 
#   subdevice to begin. The possible sources are driver-dependant. This 
#   function is only useable on subdevices that provide support for the 
#   INSN_CONFIG_ARM configuration instruction.
#
# Return value
#
#   0 on success, -1 on error.


comedi_arm = _grab("comedi_arm")
comedi_arm.restype = c_int                                                      #   int comedi_arm(
comedi_arm.argtypes = [ POINTER(comedi_t),                                      #       comedi_t * device,
                        c_uint,                                                 #       unsigned int subdevice,
                        c_uint ]                                                #       unsigned int source);

##############################################################################
# comedi_get_clock_source — get master clock for a subdevice
#
#   #include <comedilib.h>
#
#   int comedi_get_clock_source(	comedi_t * device,
#       unsigned int subdevice,
#       unsigned int channel,
#       unsigned int * clock,
#       unsigned int * period_ns);
#
# Description
#
#   This function queries the master clock for a subdevice, as set by 
#   comedi_set_clock_source. The currently configured master clock will be 
#   written to *clock. The possible values and their corresponding clocks are 
#   driver-dependant. The period of the clock in nanoseconds (or zero if it is 
#   unknown) will be written to *period_ns. If the subdevice does not support 
#   configuring its master clocks on a per-channel basis, then the channel 
#   parameter will be ignored.
#
#   It is safe to pass NULL pointers as the clock or period_ns parameters. 
#   This function is only useable on subdevices that provide support for the 
#   INSN_CONFIG_GET_CLOCK_SOURCE configuration instruction.
#
# Return value
#
#   0 on success, -1 on error.

comedi_get_clock_source = _grab("comedi_get_clock_source")
comedi_get_clock_source.restype = c_int                                         #   int comedi_get_clock_source(
comedi_get_clock_source.argtypes = [ POINTER(comedi_t),                         #       comedi_t * device,
                                     c_uint,                                    #       unsigned int subdevice,
                                     c_uint,                                    #       unsigned int channel,
                                     POINTER(c_uint),                           #       unsigned int * clock,
                                     POINTER(c_uint) ]                          #       unsigned int * period_ns);

##############################################################################
# comedi_get_gate_source — get gate for a subdevice
#
#   #include <comedilib.h>
#
#   int comedi_get_gate_source(	comedi_t * device,
#       unsigned int subdevice,
#       unsigned int channel,
#       unsigned int gate_index,
#       unsigned int * gate_source);
#
# Description
#
#   This function queries the gate for a subdevice, as set by 
#   comedi_set_gate_source. The currently configured gate source will be 
#   written to *gate_source. The possible values and their corresponding gates 
#   are driver-dependant. If the subdevice does not support configuring its 
#   gates on a per-channel basis, then the channel parameter will be ignored.
#
#   This function is only useable on subdevices that provide support for the 
#   INSN_CONFIG_GET_GATE_SOURCE configuration instruction.
#
# Return value
#
#   0 on success, -1 on error.

comedi_get_gate_source = _grab("comedi_get_gate_source")
comedi_get_gate_source.restype = c_int                                          #   int comedi_get_gate_source(
comedi_get_gate_source.argtypes = [ POINTER(comedi_t),                          #       comedi_t * device,
                                    c_uint,                                     #       unsigned int subdevice,
                                    c_uint,                                     #       unsigned int channel,
                                    c_uint,                                     #       unsigned int gate_index,
                                    POINTER(c_uint) ]                           #       unsigned int * gate_source);


##############################################################################
# comedi_get_hardware_buffer_size — get size of subdevice's hardware buffer
#
#   #include <comedilib.h>
#
#   int comedi_get_hardware_buffer_size(	comedi_t *device,
#       unsigned int subdevice,
#       enum comedi_io_direction direction);
#
# Description
#
#   This function returns the number of bytes the subdevice can hold in it's 
#   hardware buffer. The term “hardware buffer” refers to any FIFOs, etc. on 
#   the acquisition board itself which are used during streaming commands. 
#   This does not include the buffer maintained by the comedi kernel module in 
#   host memory, whose size may be queried by comedi_get_buffer_size. The 
#   direction parameter of type enum comedi_io_direction should be set to 
#   COMEDI_INPUT to query the input buffer size (e.g., the buffer of an analog 
#   input subdevice), or COMEDI_OUTPUT to query the output buffer size (e.g., 
#   the buffer of an analog output).
#
# Return value
#
#   Hardware buffer size in bytes, or -1 on error.

comedi_get_hardware_buffer_size = _grab("comedi_get_hardware_buffer_size")
comedi_get_hardware_buffer_size.restype = c_int                                 #   int comedi_get_hardware_buffer_size(
comedi_get_hardware_buffer_size.argtypes =  [ POINTER(comedi_t),                #       comedi_t *device,
                                              c_uint,                           #       unsigned int subdevice,
                                              comedi_io_direction ]             #       enum comedi_io_direction direction);


##############################################################################
# comedi_get_routing — get routing for an output
#
#   #include <comedilib.h>
#
#   int comedi_get_routing(	comedi_t * device,
#       unsigned int subdevice,
#       unsigned int channel,
#       unsigned int * routing);
#
# Description
#
#   This function queries the routing for an output, as set by 
#   comedi_set_routing. The currently configured routing will be written to 
#   *routing. The possible values and their corresponding routings are 
#   driver-dependant.
#
#   This function is only useable on subdevices that provide support for the 
#   INSN_CONFIG_GET_ROUTING configuration instruction.
#
# Return value
#
#   0 on success, -1 on error.

comedi_get_routing = _grab("comedi_get_routing")
comedi_get_routing.restype = c_int                                              #   int comedi_get_routing(
comedi_get_routing.argyptes = [ POINTER(comedi_t),                              #       comedi_t * device,
                                c_uint,                                         #       unsigned int subdevice,
                                c_uint,                                         #       unsigned int channel,
                                POINTER(c_uint) ]                               #       unsigned int * routing);


##############################################################################
# comedi_reset — reset a subdevice
#
#   #include <comedilib.h>
#
#   int comedi_reset(	comedi_t * device,
#       unsigned int subdevice);
#
# Description
#
#   This function resets a subdevice. It is only useable on subdevices that 
#   provide support for the INSN_CONFIG_RESET configuration instruction.
#
# Return value
#
#   0 on success, -1 on error.

comedi_reset = _grab("comedi_reset")
comedi_reset.restype = c_int                                                    #   int comedi_reset(
comedi_reset.argtypes = [ POINTER(comedi_t),                                    #       comedi_t * device,
                          c_uint ]                                              #       unsigned int subdevice);


##############################################################################
# comedi_set_clock_source — set master clock for a subdevice
#
# #include <comedilib.h>
#
#   int comedi_set_clock_source(	comedi_t * device,
#       unsigned int subdevice,
#       unsigned int channel,
#       unsigned int clock,
#       unsigned int period_ns);
#
# Description
#
#   This function selects a master clock for a subdevice. The clock parameter 
#   selects the master clock, and is driver-dependant. If the subdevice does 
#   not support configuring its master clocks on a per-channel basis, then the 
#   channel parameter will be ignored. The period_ns parameter specifies the 
#   clock's period in nanoseconds. It may left unspecified by using a value of 
#   zero. Drivers will ignore the clock period if they already know what the 
#   clock period should be for the specified clock (e.g. for an on-board 20MHz 
#   oscillator). Certain boards which use a phase-locked loop to synchronize to 
#   external clock sources must be told the period of the external clock. 
#   Specifying a clock period for an external clock may also allow the driver 
#   to support TRIG_TIMER sources in commands while using the external clock.
#
#   The clock may be queried with the comedi_get_clock_source function.
#
#   This function is only useable on subdevices that provide support for the 
#   INSN_CONFIG_SET_CLOCK_SOURCE configuration instruction.
#
# Return value
#
#   0 on success, -1 on error.


comedi_set_clock_source = _grab("comedi_set_clock_source")
comedi_set_clock_source.restype =  c_int                                        #   int comedi_set_clock_source(
comedi_set_clock_source.argtypes = [ POINTER(comedi_t),                         #       comedi_t * device,
                                     c_uint,                                    #       unsigned int subdevice,
                                     c_uint,                                    #       unsigned int channel,
                                     c_uint,                                    #       unsigned int clock,
                                     c_uint ]                                   #       unsigned int period_ns);



##############################################################################
# comedi_set_counter_mode — change mode of a counter subdevice
#
#   #include <comedilib.h>
#
#   int comedi_set_counter_mode(	comedi_t * device,
#       unsigned int subdevice,
#       unsigned int channel,
#       unsigned int mode);
#
# Description
#
#   This function configures a counter subdevice. The meaning of the mode 
#   parameter is driver-dependent. If the subdevice does not support 
#   configuring its mode on a per-channel basis, then the channel parameter 
#   will be ignored.
#
#   It is only useable on subdevices that provide support for the 
#   INSN_CONFIG_SET_COUNTER_MODE configuration instruction.
#
# Return value
#
#   0 on success, -1 on error.

comedi_set_counter_mode = _grab("comedi_set_counter_mode")
comedi_set_counter_mode.restype = c_int                                         #   int comedi_set_counter_mode(
comedi_set_counter_mode.argtypes = [ POINTER(comedi_t),                         #       comedi_t * device,
                                     c_uint,                                    #       unsigned int subdevice,
                                     c_uint,                                    #       unsigned int channel,
                                     c_uint ]                                   #       unsigned int mode);


##############################################################################
# comedi_set_filter — select a filter for a subdevice
#
#   #include <comedilib.h>
#
#   int comedi_set_filter(	comedi_t * device,
#       unsigned int subdevice,
#       unsigned int channel,
#       unsigned int filter);
#
# Description
#
#   This function selects a filter for a subdevice. For instance, a digital 
#   input subdevice may provide deglitching filters with varying cutoff 
#   frequencies. The filters are used to prevent high-frequency noise from 
#   causing unwanted transitions on the digital inputs. This function can tell 
#   the hardware which deglitching filter to use, or to use none at all.
#
#   The filter parameter selects which of the subdevice's filters to use, 
#   and is driver-dependant.
#
#   This function is only useable on subdevices that provide support for the 
#   INSN_CONFIG_FILTER configuration instruction.
#
# Return value
#
#   0 on success, -1 on error.

comedi_set_filter = _grab("comedi_set_filter")
comedi_set_filter.restype = c_int                                               #   int comedi_set_filter(
comedi_set_filter.argtypes = [ POINTER(comedi_t),                               #       comedi_t * device,
                               c_uint,                                          #       unsigned int subdevice,
                               c_uint,                                          #       unsigned int channel,
                               c_uint ]                                         #       unsigned int filter);



##############################################################################
# comedi_set_gate_source — select gate source for a subdevice
#
#   #include <comedilib.h>
#
#   int comedi_set_gate_source(	comedi_t * device,
#       unsigned int subdevice,
#       unsigned int channel,
#       unsigned int gate_index,
#       unsigned int gate_source);
#
# Description
#
#   This function selects a gate source for a subdevice. The gate_index 
#   parameter selects which gate is being configured, should the subdevice 
#   have multiple gates. It takes a value from 0 to N-1 for a subdevice with N 
#   different gates. The gate_source parameter selects which signal you wish 
#   to use as the gate, and is also driver-dependent. If the subdevice does 
#   not support configuring its gates on a per-channel basis, then the channel 
#   parameter will be ignored.
#
#   You may query the gate source with the comedi_get_gate_source function. 
#   This function is only useable on subdevices that provide support for the 
#   INSN_CONFIG_SET_GATE_SOURCE configuration instruction.
#
# Return value
#
#   0 on success, -1 on error.

comedi_set_gate_source = _grab("comedi_set_gate_source")
comedi_set_gate_source = c_int                                                  #   int comedi_set_gate_source(
comedi_set_gate_source = [ POINTER(comedi_t),                                   #       comedi_t * device,
                           c_uint,                                              #       unsigned int subdevice,
                           c_uint,                                              #       unsigned int channel,
                           c_uint,                                              #       unsigned int gate_index,
                           c_uint ]                                             #       unsigned int gate_source);



##############################################################################
# comedi_set_other_source — select source signal for something other than a gate or clock
#
#   #include <comedilib.h>
#
#   int comedi_set_other_source(	comedi_t * device,
#       unsigned int subdevice,
#       unsigned int channel,
#       unsigned int other,
#       unsigned int source);
#
# Description
#
#   This function allows selection of a source signal for something on a 
#   subdevice other than a gate (which uses comedi_set_gate_source) or a clock 
#   (which uses comedi_set_clock_source). The other parameter selects which 
#   “other” we are configuring, and is driver-dependent. The source parameter 
#   selects the source we which to use for the “other”. If the subdevice does 
#   not support configuring its “other” sources on a per-channel basis, then 
#   the channel parameter will be ignored.
#
#   As an example, this function is used to select which PFI digital input 
#   channels should be used as the A/B/Z signals when running a counter on an 
#   NI M-Series board as a quadrature encoder. The other parameter selects 
#   either the A, B, or Z signal, and the source parameter is used to specify 
#   which PFI digital input channel the external A, B, or Z signal is 
#   physically connected to.
#
#   This function is only useable on subdevices that provide support for the 
#   INSN_CONFIG_SET_OTHER_SOURCE configuration instruction.
#
# Return value
#
#   0 on success, -1 on error.

comedi_set_other_source = _grab("comedi_set_other_source")
comedi_set_other_source.restype = c_int                                         #   int comedi_set_other_source(
comedi_set_other_source.argtypes = [ POINTER(comedi_t),                         #       comedi_t * device,
                                   c_uint,                                      #       unsigned int subdevice,
                                   c_uint,                                      #       unsigned int channel,
                                   c_uint,                                      #       unsigned int other,
                                   c_uint ]                                     #       unsigned int source);



##############################################################################
# comedi_set_routing — select a routing for an output
#
#   #include <comedilib.h>
#
#   int comedi_set_routing(	comedi_t * device,
#       unsigned int subdevice,
#       unsigned int channel,
#       unsigned int routing);
#
# Description
#
#   This function configures a mutiplexed output channel which can output a 
#   variety of different signals (such as NI's RTSI and PFI lines). The routing 
#   parameter selects which signal should be routed to appear on the selected 
#   output channel, and is driver-dependant.
#
#   The routing may be queried with the comedi_get_routing function. This 
#   function is only useable on subdevices that provide support for the 
#   INSN_CONFIG_SET_ROUTING configuration instruction.
#
# Return value
#
#   0 on success, -1 on error.

comedi_set_routing = _grab("comedi_set_routing")
comedi_set_routing.restype = c_int                                              #   int comedi_set_routing(
comedi_set_routing.argtypes = [ POINTER(comedi_t),                              #       comedi_t * device,
                                c_uint,                                         #       unsigned int subdevice,
                                c_uint,                                         #       unsigned int channel,
                                c_uint ]                                        #       unsigned int routing);



##############################################################################
#                   - Begin DEPRECATED FUNCTIONS section -
##############################################################################
#  
    

##############################################################################
# comedi_dio_bitfield — read/write multiple digital channels
#
#   #include <comedilib.h>
#
#   int comedi_dio_bitfield(	comedi_t * device,
#       unsigned int subdevice,
#       unsigned int write_mask,
#       unsigned int * bits);
#
# Description
#
#   This function is deprecated. Use comedi_dio_bitfield2 instead. It is 
#   equivalent to using comedi_dio_bitfield2 with base_channel set to 0.


if import_deprecated:
    comedi_dio_bitfield = _grab("comedi_dio_bitfield")
    comedi_dio_bitfield.restype = c_int                                         #   int comedi_dio_bitfield(
    comedi_dio_bitfield.argtypes = [ POINTER(comedi_t),                         #       comedi_t * device,
                                     c_uint,                                    #       unsigned int subdevice,
                                     c_uint,                                    #       unsigned int write_mask,
                                     POINTER(c_uint) ]                          #       unsigned int * bits);


##############################################################################
# comedi_get_timer — timer information (deprecated)
#
#   #include <comedilib.h>
#
#   int comedi_get_timer(	comedi_t * device,
#       unsigned int subdevice,
#       double frequency,
#       unsigned int * trigvar,
#       double * actual_frequency);
#
# Description
#
#   The function comedi_get_timer converts the frequency frequency to a number 
#   suitable to send to the driver in a comedi_trig structure. This function 
#   remains for compatibility with very old versions of Comedi, that converted 
#   sampling rates to timer values in the library. This conversion is now done 
#   in the kernel, and every device has the timer type nanosec_timer, indicating 
#   that timer values are simply a time specified in nanoseconds.

if import_deprecated:
    comedi_get_timer = _grab("comedi_get_timer")
    comedi_get_timer.restype = c_int                                            #   int comedi_get_timer(
    comedi_get_timer.argtypes = [ POINTER(comedi_t),                            #       comedi_t * device,
                                  c_uint,                                       #       unsigned int subdevice,
                                  c_double,                                     #       double frequency,
                                  POINTER(c_uint),                              #       unsigned int * trigvar,
                                  POINTER(c_double) ]                           #       double * actual_frequency);



##############################################################################
# comedi_sv_init — slowly-varying inputs
#
#   #include <comedilib.h>
#
#   int comedi_sv_init(	comedi_sv_t * sv,
#       comedi_t * device,
#       unsigned int subdevice,
#       unsigned int channel);
#
# Description
#
#   The function comedi_sv_init initializes the slow varying Comedi structure 
#   pointed to by sv to use the device device, the analog input subdevice 
#   subdevice, and the channel channel. The slow varying Comedi structure is 
#   used by comedi_sv_measure to accurately measure an analog input by 
#   averaging over many samples. The default number of samples is 100.
#
# Return value
#
#   This function returns 0 on success, -1 on error.

if import_deprecated:
    comedi_sv_init = _grab("comedi_sv_init")
    comedi_sv_init.restype = c_int                                              #   int comedi_sv_init(
    comedi_sv_init.argtypes = [ POINTER(comedi_sv_t),                           #       comedi_sv_t * sv,
                                POINTER(comedi_t),                              #       comedi_t * device,
                                c_uint,                                         #       unsigned int subdevice,
                                c_uint ]                                        #       unsigned int channel);


##############################################################################
# comedi_sv_measure — slowly-varying inputs
#
#   #include <comedilib.h>
#
#   int comedi_sv_measure(	comedi_sv_t * sv,
#       double * data);
#
# Description
#
#   The function comedi_sv_measure uses the slowly varying Comedi structure 
#   pointed to by sv to measure a slowly varying signal. If successful, the 
#   result (in physical units) is stored in the location pointed to by data, 
#   and the number of samples is returned. On error, -1 is returned.

if import_deprecated:
    comedi_sv_measure = _grab("comedi_sv_measure")
    comedi_sv_measure.restype = c_int                                           #   int comedi_sv_measure(
    comedi_sv_measure.argyptes = [ POINTER(comedi_sv_t),                        #       comedi_sv_t * sv,
                                   POINTER(c_double) ]                          #       double * data);


##############################################################################
# comedi_sv_update — slowly-varying inputs
#
#   #include <comedilib.h>
#
#   int comedi_sv_update(	comedi_sv_t * sv);
#
# Description
#
#   The function comedi_sv_update updates internal parameters of the slowly 
#   varying Comedi structure pointed to by sv.

if import_deprecated:
    comedi_sv_update = _grab("comedi_sv_update")
    comedi_sv_update.restype = c_int                                            #   int comedi_sv_update(
    comedi_sv_update.argyptes = [ POINTER(comedi_sv_t) ]                        #       comedi_sv_t * sv);


##############################################################################
# comedi_timed_1chan — streaming input (deprecated)
#
#   #include <comedilib.h>
#
#   int comedi_timed_1chan(	comedi_t * device,
#       unsigned int subdevice,
#       unsigned int channel,
#       unsigned int range,
#       unsigned int aref,
#       double frequency,
#       unsigned int num_samples,
#       double * data);
#
# Description
#
#   Not documented.


if import_deprecated:
    comedi_timed_1chan = _grab("comedi_timed_1chan")
    comedi_timed_1chan.restype = c_int                                          #   int comedi_timed_1chan(
    comedi_timed_1chan.argyptes = [ POINTER(comedi_t),                          #       comedi_t * device,
                                    c_uint,                                     #       unsigned int subdevice,
                                    c_uint,                                     #       unsigned int channel,
                                    c_uint,                                     #       unsigned int range,
                                    c_uint,                                     #       unsigned int aref,
                                    c_double,                                   #       double frequency,
                                    c_uint,                                     #       unsigned int num_samples,
                                    POINTER(c_double) ]                         #       double * data);



##############################################################################
# comedi_trigger — perform streaming input/output (deprecated)
#
#   #include <comedilib.h>
#
#   int comedi_trigger(	comedi_t * device,
#       comedi_trig * trig);
#
# Description
#
#   The function comedi_trigger instructs Comedi to perform the command 
#   specified by the trigger structure pointed to by trig. The return value 
#   depends on the particular trigger being issued. If there is an error, -1 
#   is returned.

if import_deprecated:
    comedi_trigger = _grab("comedi_trigger")
    comedi_trigger.restype = c_int                                              #   int comedi_trigger(
    comedi_trigger.argtypes = [ POINTER(comedi_t),                              #       comedi_t * device,
                                POINTER(comedi_trig)]                           #       comedi_trig * trig);



