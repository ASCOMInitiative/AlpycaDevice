# --------------
# SYMBOLIC ENUMS
# --------------
#
from enum import IntEnum

class AlignmentModes(IntEnum):
    algAltAz        = 0,
    algPolar        = 1,
    algGermanPolar  = 2

class DriveRates(IntEnum):
    driveSidereal   = 0,
    driveLunar      = 1,
    driveSolar      = 2,
    driveKing       = 3

class EquatorialCoordinateType(IntEnum):
    equOther        = 0,
    equTopocentric  = 1,
    equJ2000        = 2,
    equJ2050        = 3,
    equB1950        = 4

class GuideDirections(IntEnum):    # Shared by Camera
    guideNorth      = 0,
    guideSouth      = 1,
    guideEast       = 2,
    guideWest       = 3

class PierSide(IntEnum):
    pierEast        = 0,
    pierWest        = 1,
    pierUnknown     = -1

class TelescopeAxes(IntEnum):
    axisPrimary     = 0,
    axisSecondary   = 1,
    axisTertiary    = 2
