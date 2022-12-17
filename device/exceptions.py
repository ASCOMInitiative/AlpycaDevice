# =======================================
# EXCEPTIONS.PY - Alpaca Exception Casses
# =======================================
#
# 17-Dec-2022   rbd 0.1 Initial edit for Alpaca sample/template
#

DriverBase = 0x400      # Starting value for driver-specific exceptions
DriverMax = 0xFFF       # Maximum value for driver-specific excptions

class Success:
    Number = 0
    Message = ''
    
class ActionNotImplementedException:
    Number = 0x40C
    Message = 'The requested action is not implemented in this driver.'

class AlpacaRequestException:
    Number = 0x40C
    Message = 'The requested action is not implemented in this driver.'

class InvalidOperationException:
    Number = 0x40B
    Message = 'The requested operation cannot be undertaken at this time.'

class InvalidValueException:
    Number = 0x401
    Message = 'Invalid value.'

class NotConnectedException:
    Number = 0x407
    Message = 'The communications channel is not connected'

class NotImplementedException:
    Number = 0x400
    Message = 'Property or method not implemented'

class ValueNotSetException:
    Number = 0x402
    Message = 'The value has not yet been set.'
