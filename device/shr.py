# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# shr.py - Device characteristics and support classes/functions/data
#
# Part of the Alpyca-Device Alpaca skeleton/template device driver
#
# Author:   Robert B. Denny <rdenny@dc3.com> (rbd)
#
# Python Compatibility: Requires Python 3.7 or later
# GitHub: https://github.com/ASCOMInitiative/alpyca-device
#
# -----------------------------------------------------------------------------
# MIT License
#
# Copyright (c) 2022 Bob Denny
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# -----------------------------------------------------------------------------
# Edit History:
# 15-Dec-2022   rbd 0.1 Initial edit for Alpaca sample/template
# 18-Dev-2022   rbd 0.1 Additional driver info items
# 20-Dec-2022   rbd 0.1 Fix idiotic error in to_bool()
# 22-Dec-2022   rbd 0.1 DeviceMetadata
# 24-Dec-2022   rbd 0.1 Logging
# 25-Dec-2022   rbd 0.1 Logging typing for intellisense
# 26-Dec-2022   rbd 0.1 Refactor logging to conf module. 
# 27-Dec-2022   rbd 0.1 Methods can return values. Common request
#                       logging (before starting processing).
#                       MIT license and module header. Logging cleanup.
#                       Python 3.7 global restriction.
#
from threading import Lock
import exceptions
import json
from falcon import Request
from logging import Logger

#logger: Logger = None
logger = None                   # Safe on Python 3.7 but no intellisense in VSCode etc.

def set_shr_logger(lgr):
    global logger
    logger = lgr

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
def get_args_caseless(name: str, req: Request, default):
    lcName = name.lower()
    for param in req.params.items():                    # [name,value] tuples
        if param[0].lower() == lcName:
            return param[1]
    return default                                      # not in args, return default

# 
# Log the request as soon as the resource andler gets it so subsequent
# logged messages are in the right order. Logs PUT body as well.
#
def log_request(req: Request):
    msg = f'{req.remote_addr} {req.method} {req.path}'
    if not req.query_string is None:
        msg += f'?{req.query_string}'
    logger.info(msg)
    if req.method == 'PUT' and req.content_length != None:
        logger.info(f'{req.remote_addr} -> {req.media}')

# ------------------
# PropertyResponse
# ------------------

class PropertyResponse():
    def __init__(self, value, req: Request, err = exceptions.Success()):
        self.ServerTransactionID = getNextTransId()
        self.Value = value
        ctid = get_args_caseless('ClientTransactionID', req, None)
        if not ctid is None:
            self.ClientTransactionID = int(ctid)
        else:
            self.ClientTransactionID = 0        # Per Alpaca, Return a 0 if ClientTransactionId is not in the request
        self.ErrorNumber = err.Number
        self.ErrorMessage = err.Message
        if not value is None:
            logger.info(f'{req.remote_addr} <- {str(value)}')

    @property
    def json(self) -> str:
        return json.dumps(self.__dict__)

# --------------
# MethodResponse
# --------------

class MethodResponse():
    def __init__(self, req: Request, err = exceptions.Success(), value = None): # value useless unless Success
        self.ServerTransactionID = getNextTransId()
        formdata= req.get_media()
        if 'ClientTransactionID' in formdata:
            self.ClientTransactionID = int(formdata['ClientTransactionID'])
        else:
            self.ClientTransactionID = 0        # Per Alpaca, Return a 0 if ClientTransactionId is not in the request
        if not value is None:
            self.Value = value
            logger.info(f'{req.remote_addr} <- {str(value)}')

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
