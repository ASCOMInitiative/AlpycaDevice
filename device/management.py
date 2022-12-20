# ================================================
# MANAGEMENT.PY - Management API for Alpaca Device
# ================================================
#
# 17-Dec-2022   rbd 0.1 Initial edit for Alpaca sample/template
# 19-Dec-2022   rbd 0.1 Constants in shr.py
#
import falcon
from shr import *

# -----------
# APIVersions
# -----------
class apiversions():
    def on_get(self, req: falcon.Request, resp: falcon.Response):
        apis = [ 1 ]                            # TODO MAKE CONFIG OR GLOBAL
        resp.text = PropertyResponse(apis, req).json


# -----------
# Description
# -----------
class description():
    def on_get(self, req: falcon.Request, resp: falcon.Response):
        desc = {
            'ServerName' : 'Alpaca Sample Device Server', 
            'Manufacturer' : 'ASCOM Initiative',
            'ManufacturerVersion' : s_DriverVersion,
            'Location' : 'Alvord Desert' 
            }
        resp.text = PropertyResponse(desc, req).json

# -----------------
# ConfiguredDevices
# -----------------
class configureddevices():
    def on_get(self, req: falcon.Request, resp: falcon.Response):
        confarray = [                          # TODO ADD ONE FOR EACH DEVICE (ANY TYPE) SERVED
            {
            'DeviceName'    : s_DriverDescription, 
            'DeviceType'    : s_DriverType,
            'DeviceNumber'  : 0,
            'UniqueID'      : s_DriverID 
            }
        ]
        resp.text = PropertyResponse(confarray, req).json
