#
# 15-Dec-2022   rbd 0.1 Initial edit for Alpaca sample/template
# 18-Dev-2022   rbd 0.1 Additional driver info items
# 20-Dec-2022   rbd 0.1 Fix idiotic error in to_bool()
# 22-Dec-2022   rbd 0.1 DeviceMetadata
# 24-Dec-2022   rbd 0.1 Logging
# 25-Dec-2022   rbd 0.1 Logging typing for intellisense
# 26-Dec-2022   rbd 0.1 Refacor logging to conf module
#
from threading import Lock
import exceptions
import json
import falcon
# from logging import Logger

# logger: Logger = None   # Set to global logger at app startup

# def set_shr_logger(lgr):
#     global logger
#     logger = lgr

# ---------------
# Data Validation
# ---------------
bools = ['true', 'false']                               # Only valid JSON bools allowed
def to_bool(str: str) -> bool:
    val = str.lower()
    if val not in bools:
        raise ValueError
    return val == bools[0]

# -----------
# Device Info
# -----------
# Static metadata not subject to configuration changes
class DeviceMetadata:
    Name = 'Sample Rotator'
    Version = '0.1'
    Description = 'Alpaca Sample Rotator '
    Type = 'Rotator'
    ID = '1892ED30-92F3-4236-843E-DA8EEEF2D1CC' # https://guidgenerator.com/online-guid-generator.aspx
    Info = 'Alpaca Sample Device\nImplements Rotator\nASCOM Initiative'
    Manufacturer = 'ASCOM Initiative'
    InterfaceVersion = 3        # IRotatorV3


#
# Get query string item with case-insensitive name
# These must be caseless per the Alpaca spec
#
def get_args_caseless(name: str, req: falcon.Request, default):
    lcName = name.lower()
    for param in req.params.items():                    # [name,value] tuples
        if param[0].lower() == lcName:
            return param[1]
    return default                                      # not in args, return default


# ------------------
# PropertyResponse
# ------------------

class PropertyResponse():
    def __init__(self, value, req: falcon.Request, err = exceptions.Success()):
        self.ServerTransactionID = getNextTransId()
        self.Value = value
        ctid = get_args_caseless('ClientTransactionID', req, None)
        if not ctid is None:
            self.ClientTransactionID = int(ctid)
        else:
            self.ClientTransactionID = 0        # Per Alpaca, Return a 0 if ClientTransactionId is not in the request
        self.ErrorNumber = err.Number
        self.ErrorMessage = err.Message

    @property
    def json(self) -> str:
        return json.dumps(self.__dict__)

# --------------
# MethodResponse
# --------------

class MethodResponse():
    def __init__(self, formdata, err = exceptions.Success()):
        self.ServerTransactionID = getNextTransId()
        if 'ClientTransactionID' in formdata:
            self.ClientTransactionID = int(formdata['ClientTransactionID'])
        else:
            self.ClientTransactionID = 0        # Per Alpaca, Return a 0 if ClientTransactionId is not in the request
        self.ErrorNumber = err.Number
        self.ErrorMessage = err.Message
        
    @property
    def json(self) -> str:
        return json.dumps(self.__dict__)



# -------------------------------
# Thread-safe ServerTransactionID
# -------------------------------
_lock = Lock()
_stid = 0

def getNextTransId():
    with _lock:
        global _stid
        _stid += 1
    return _stid
