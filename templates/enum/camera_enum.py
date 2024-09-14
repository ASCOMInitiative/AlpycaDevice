# --------------
# SYMBOLIC ENUMS
# --------------
#
from enum import IntEnum

class CameraStates(IntEnum):
    cameraIdle      = 0,
    cameraWaiting   = 1,
    cameraExposing  = 2,
    cameraReading   = 3,
    cameraDownload  = 4,
    cameraError     = 5

class SensorType(IntEnum):
    Monochrome      = 0,
    Color           = 1,
    RGGB            = 2,
    CMYG            = 3,
    CMYG2           = 4,
    LRGB            = 5

class ImageArrayElementTypes(IntEnum):
    Unknown         = 0
    Int16           = 1
    Int32           = 2
    Double          = 3
    Single          = 4,
    UInt64          = 5,
    Byte            = 6,
    Int64           = 7,
    UInt16          = 8
