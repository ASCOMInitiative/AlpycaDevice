# ================================================
# MANAGEMENT.PY - Management API for Alpaca Device
# ================================================
#
# 17-Dec-2022   rbd 0.1 Initial edit for Alpaca sample/template
#
import falcon
from shr import PropertyResponse, s_DriverVersion

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
            'ManufacturerVersion' : '0.1',      # TODO MAKE CONF OR GLOBAL, USE SEMVER
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
            'DeviceName' : 'Alpaca Sample Device', 
            'DeviceType' : 'Rotator',
            'DeviceNumber' : 0,
            'UniqueID' : '1892ED30-92F3-4236-843E-DA8EEEF2D1CC' # https://guidgenerator.com/online-guid-generator.aspx
            }
        ]
        resp.text = PropertyResponse(confarray, req).json
