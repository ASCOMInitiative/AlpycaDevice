# --------------
# SYMBOLIC ENUMS
# --------------
#
from enum import IntEnum

class CalibratorStatus(IntEnum):
    NotPresent = 0,
    Off = 1,
    NotReady = 2,
    Ready = 3,
    Unknown = 4,
    Error = 5

class CoverStatus(IntEnum):
    NotPresent = 0,
    Closed = 1,
    Moving = 2,
    Open = 3,
    Unknown = 4,
    Error = 5
