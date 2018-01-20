import ctypes

class UnicornProto(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
            ("device", ctypes.c_char *24),
            ("timestamp", ctypes.c_int),
            ("temperature", ctypes.c_float),
            ("pressure", ctypes.c_float),
            ("humidity", ctypes.c_float),
            ("CO2", ctypes.c_float),
            ("light", ctypes.c_short),
            ("battery", ctypes.c_ubyte),
            ("snow_intensity", ctypes.c_short),
            ("rain_intensity", ctypes.c_short),
            ("result", ctypes.c_short),
    ]