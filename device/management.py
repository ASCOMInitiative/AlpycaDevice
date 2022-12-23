# ================================================
# MANAGEMENT.PY - Management API for Alpaca Device
# ================================================
#
# 17-Dec-2022   rbd 0.1 Initial edit for Alpaca sample/template
# 19-Dec-2022   rbd 0.1 Constants in shr.py
# 22-Dec-2022   rbd 0.1 Device metadata, Configuration
#
import falcon
from shr import PropertyResponse, DeviceMetadata
from conf import Config

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
            'ServerName'   : DeviceMetadata.Description,
            'Manufacturer' : DeviceMetadata.Manufacturer,
            'Version'      : DeviceMetadata.Version,
            'Location'     : Config.location
            }
        resp.text = PropertyResponse(desc, req).json

# -----------------
# ConfiguredDevices
# -----------------
class configureddevices():
    def on_get(self, req: falcon.Request, resp: falcon.Response):
        confarray = [                          # TODO ADD ONE FOR EACH DEVICE (ANY TYPE) SERVED
            {
            'DeviceName'    : DeviceMetadata.Name, 
            'DeviceType'    : DeviceMetadata.Type,
            'DeviceNumber'  : 0,
            'UniqueID'      : DeviceMetadata.ID 
            }
        ]
        resp.text = PropertyResponse(confarray, req).json
