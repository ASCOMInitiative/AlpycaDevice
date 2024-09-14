# --------------
# SYMBOLIC ENUMS
# --------------
#
from enum import IntEnum

class ShutterState(IntEnum):
    shutterOpen     = 0,
    shutterClosed   = 1,
    shutterOpening  = 2,
    shutterClosing  = 3,
    shutterError    = 4
