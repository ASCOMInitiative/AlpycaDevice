#
# 15-Dec-2022   rbd 0.1 Initial edit for Alpaca sample/template
#
from threading import Lock
import exceptions
import json
import falcon

# ---------------
# Data Validation
# ---------------
bools = ['true', 'false']                               # Only valid JSON bools allowed
def to_bool(str) -> bool:
    if str not in bools:
        raise ValueError
    return str == bools[0]

# -----------
# Driver Info
# -----------
s_DriverName = 'Sample Rotator'
s_DriverVersion = '0.1'
s_DriverDescription = 'Alpaca Sample Rotator Device'
s_DriverType = 'Rotator'
s_DriverID = '1892ED30-92F3-4236-843E-DA8EEEF2D1CC' # https://guidgenerator.com/online-guid-generator.aspx
s_DriverInfo = ['Alpaca Sample Device', 'Implements Rotator', 'ASCOM Initiative']
s_DriverInterfaceVersion = 3        # IRotatorV3


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
            self.ClientTransactionID = ctid
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
            self.ClientTransactionID = formdata['ClientTransactionID']
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
        global _stid                            # TODO Why this and not _lock?!?!?!?
        _stid += 1
    return _stid
