# ==============================================================
# COMMON.PY - Endpoints for members common to all Alpaca devices
# ==============================================================
#
# 16-Dec-2022   rbd 0.1 Initial edit for Alpaca sample/template
# 18-Dec-2022   rbd 0.1 Implement remaining controller classes
# 20-Dec-2022   rbd 0.1 Fix SupportedActions ha ha.
#
import falcon
from exceptions import *
from shr import *
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
        resp.text = PropertyResponse(s_DriverDescription, req).json

class DriverInfo():
    def on_get(self, req: falcon.Request, resp: falcon.Response):
        resp.text = PropertyResponse(s_DriverInfo, req).json

class InterfaceVersion():
    def on_get(self, req: falcon.Request, resp: falcon.Response):
        resp.text = PropertyResponse(s_DriverInterfaceVersion, req).json

class DriverVersion():
    def on_get(self, req: falcon.Request, resp: falcon.Response):
        resp.text = PropertyResponse(s_DriverVersion, req).json

class Name():
    def on_get(self, req: falcon.Request, resp: falcon.Response):
        resp.text = PropertyResponse(s_DriverName, req).json

class SupportedActions():
    def on_get(self, req: falcon.Request, resp: falcon.Response):
        resp.text = PropertyResponse([], req).json  # Not PropertyNotImplemented

