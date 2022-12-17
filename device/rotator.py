# =================================================================
# ROTATOR.PY - Endpoints for members of ASCOM Alpaca Rotator Device
# =================================================================
#
# 16-Dec-2022   rbd 0.1 Initial edit for Alpaca sample/template
#
import falcon
from shr import PropertyResponse, MethodResponse, to_bool
from rotatordevice import RotatorDevice
from exceptions import InvalidValueException

# --------------------
# SIMULATED ROTATOR ()
# --------------------
rot_dev = RotatorDevice()             # Start it up now

# RESOURCE CONTROLLERS
# --------------------

class CanReverse():
    def on_get(self, req: falcon.Request, resp: falcon.Response):
        resp.text = PropertyResponse(True, req).json

class Connected:
    def on_get(self, req: falcon.Request, resp: falcon.Response):
        resp.text = PropertyResponse(rot_dev.connected, req).json

    def on_put(self, req: falcon.Request, resp: falcon.Response):
        formdata = req.get_media()
        try:
            conn = to_bool(formdata['Connected'])
        except:
            resp.text = MethodResponse(formdata, InvalidValueException).json
            return
        print (f'Connected = {conn}) from ClientID={formdata["ClientID"]}')
        rot_dev.connected = conn
        resp.text = MethodResponse(formdata).json

class MoveAbsolute():
    def on_put(self, req: falcon.Request, resp: falcon.Response):
        formdata = req.get_media()
        try:
            newpos = float(formdata['Position'])
        except:
            resp.text = MethodResponse(formdata, InvalidValueException).json
            return
        print (f'MoveAbsolute({newpos}) from ClientID={formdata["ClientID"]}')
        # At this point change the state of the switch
        resp.text = MethodResponse(formdata).json
