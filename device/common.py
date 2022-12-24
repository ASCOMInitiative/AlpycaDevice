# ==============================================================
# COMMON.PY - Endpoints for members common to all Alpaca devices
# ==============================================================
#
# 16-Dec-2022   rbd 0.1 Initial edit for Alpaca sample/template
# 18-Dec-2022   rbd 0.1 Implement remaining controller classes
# 20-Dec-2022   rbd 0.1 Fix SupportedActions ha ha.
# 22-Dec-2022   rbd 0.1 Refectored metadata support
#
import falcon
import logging
from exceptions import *    # Only exception classes here
from shr import PropertyResponse, MethodResponse, DeviceMetadata

logger = logging.getLogger(__name__)

# --------------------
# RESOURCE CONTROLLERS
# --------------------

class Action():
    def on_put(self, req: falcon.Request, resp: falcon.Response):
        formdata = req.get_media()
        resp.text = MethodResponse(formdata, NotImplementedException()).json

class CommandBlind():
    def on_put(self, req: falcon.Request, resp: falcon.Response):
        formdata = req.get_media()
        resp.text = MethodResponse(formdata, NotImplementedException()).json

class CommandBool():
    def on_put(self, req: falcon.Request, resp: falcon.Response):
        formdata = req.get_media()
        resp.text = MethodResponse(formdata, NotImplementedException()).json

class CommandString():
    def on_put(self, req: falcon.Request, resp: falcon.Response):
        formdata = req.get_media()
        resp.text = MethodResponse(formdata, NotImplementedException()).json

# Connected, though common, is implemented in rotator.py
class Description():
    def on_get(self, req: falcon.Request, resp: falcon.Response):
        resp.text = PropertyResponse(DeviceMetadata.Description, req).json

class DriverInfo():
    def on_get(self, req: falcon.Request, resp: falcon.Response):
        resp.text = PropertyResponse(DeviceMetadata.Info, req).json

class InterfaceVersion():
    def on_get(self, req: falcon.Request, resp: falcon.Response):
        resp.text = PropertyResponse(DeviceMetadata.InterfaceVersion, req).json

class DriverVersion():
    def on_get(self, req: falcon.Request, resp: falcon.Response):
        logger.info('DriverVersion')
        resp.text = PropertyResponse(DeviceMetadata.Version, req).json

class Name():
    def on_get(self, req: falcon.Request, resp: falcon.Response):
        resp.text = PropertyResponse(DeviceMetadata.Name, req).json

class SupportedActions():
    def on_get(self, req: falcon.Request, resp: falcon.Response):
        resp.text = PropertyResponse([], req).json  # Not PropertyNotImplemented

