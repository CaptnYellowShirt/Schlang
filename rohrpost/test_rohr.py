# -*- coding: utf-8 -*-


from ctypes import *


class tubeID(Structure):
    _fields_ = [("mouth", c_int),
                ("tail", c_int),
                ("threadNo", c_ulong),
                ("bytesMoved", c_double),
                ("tubeStatus", c_uint),
                ("tubeCmd", c_uint)]



_pTube = tubeID()
pTube = pointer(_pTube)


_librohrpost = CDLL('./librohrpost.so')

_grab = _librohrpost.__getitem__


laytube_toFile = _grab("laytube_toFile")
laytube_toFile.restype = c_int
laytube_toFile.argtypes = [POINTER(tubeID)]

    

