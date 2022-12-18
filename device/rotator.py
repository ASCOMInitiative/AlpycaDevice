# =================================================================
# ROTATOR.PY - Endpoints for members of ASCOM Alpaca Rotator Device
# =================================================================
#
# 16-Dec-2022   rbd 0.1 Initial edit for Alpaca sample/template
# 18-Dec-2022   rbd 0.1 For upgraded exception classes
#
import falcon
from shr import PropertyResponse, MethodResponse, to_bool
from rotatordevice import RotatorDevice
from exceptions import InvalidValueException, NotConnectedException, DriverException
import sys 
import traceback


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
            resp.text = MethodResponse(formdata, 
                            InvalidValueException('Connected must be set to true or false')).json
            return
        print (f'Connected = {conn}) from ClientID={formdata["ClientID"]}')
        try:
            # ----------------------
            rot_dev.connected = conn
            # ----------------------
        except Exception as ex:
            resp.text = MethodResponse(formdata, # Put is actually like a method :-(
                            DriverException(0x500, '{self.__class__.__name__} failed', ex)).json
            return
        resp.text = MethodResponse(formdata).json

class MoveAbsolute():
    def on_put(self, req: falcon.Request, resp: falcon.Response):
        formdata = req.get_media()
        if not rot_dev.connected:
            resp.text = MethodResponse(formdata, 
                            NotConnectedException()).json
            return
        try:
            newpos = float(formdata['Position'])
        except:
            resp.text = MethodResponse(formdata, 
                            InvalidValueException('Position not a valid integer.')).json
            return
        if newpos < 0.0 or newpos >= 360.0:
            resp.text = MethodResponse(formdata, 
                            InvalidValueException('Invalid position outside range 0 <= pos < 360.')).json
            return
        print (f'MoveAbsolute({newpos}) from ClientID={formdata["ClientID"]}')
        try:
            # --------------------------
            rot_dev.MoveAbsolute(newpos)    # async
            # --------------------------
        except Exception as ex:
            resp.text = MethodResponse(formdata, # Put is actually like a method :-(
                            DriverException(0x500, '{self.__class__.__name__} failed', ex)).json
            return
        resp.text = MethodResponse(formdata).json
