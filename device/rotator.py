# =================================================================
# ROTATOR.PY - Endpoints for members of ASCOM Alpaca Rotator Device
# =================================================================
#
# 16-Dec-2022   rbd 0.1 Initial edit for Alpaca sample/template
# 18-Dec-2022   rbd 0.1 For upgraded exception classes
# 19-Dec-2022   rbd 0.1 Implement all IRotatorV3 endpoints
#
import falcon
from shr import *
from exceptions import *
from rotatordevice import RotatorDevice


# --------------------
# SIMULATED ROTATOR ()
# --------------------
rot_dev = RotatorDevice()             # Start it up now

# --------------------
# RESOURCE CONTROLLERS
# --------------------
class CanReverse:
    def on_get(self, req: falcon.Request, resp: falcon.Response):
        resp.text = PropertyResponse(True, req).json    # IRotatorV3, CanReverse must be True

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
                            DriverException(0x500, f'{self.__class__.__name__} failed', ex)).json
            return
        resp.text = MethodResponse(formdata).json

class IsMoving:
    def on_get(self, req: falcon.Request, resp: falcon.Response):
        if not rot_dev.connected:
            resp.text = PropertyResponse(None, req, 
                            NotConnectedException()).json
            return
        try:
            # ---------------------
            pos = rot_dev.is_moving
            # ---------------------
        except Exception as ex:
            resp.text = PropertyResponse(None, req, 
                            DriverException(0x500, f'{self.__class__.__name__} failed', ex)).json
            return
        resp.text = PropertyResponse(pos, req).json

class MechanicalPosition:
    def on_get(self, req: falcon.Request, resp: falcon.Response):
        if not rot_dev.connected:
            resp.text = PropertyResponse(None, req, 
                            NotConnectedException()).json
            return
        try:
            # -------------------------------
            pos = rot_dev.mechanical_position
            # -------------------------------
        except Exception as ex:
            resp.text = PropertyResponse(None, req, 
                            DriverException(0x500, f'{self.__class__.__name__} failed', ex)).json
            return
        resp.text = PropertyResponse(pos, req).json

class Reverse:
    def on_get(self, req: falcon.Request, resp: falcon.Response):
        if not rot_dev.connected:
            resp.text = PropertyResponse(None, req, 
                            NotConnectedException()).json
            return
        try:
            # -------------------
            rev = rot_dev.reverse
            # -------------------
        except Exception as ex:
            resp.text = PropertyResponse(None, req, 
                            DriverException(0x500, f'{self.__class__.__name__} failed', ex)).json
            return
        resp.text = PropertyResponse(rev, req).json

    def on_put(self, req: falcon.Request, resp: falcon.Response):
        formdata = req.get_media()
        if not rot_dev.connected:
            resp.text = MethodResponse(formdata, 
                            NotConnectedException()).json
            return
        try:
            rev = to_bool(formdata['Reverse'])
        except:
            resp.text = MethodResponse(formdata, 
                            InvalidValueException('Reverse must be set to true or false')).json
            return
        print (f'Connected = {rev}) from ClientID={formdata["ClientID"]}')
        try:
            # ----------------------
            rot_dev.reverse = rev
            # ----------------------
        except Exception as ex:
            resp.text = MethodResponse(formdata, # Put is actually like a method :-(
                            DriverException(0x500, f'{self.__class__.__name__} failed', ex)).json
            return
        resp.text = MethodResponse(formdata).json

class StepSize:
    def on_get(self, req: falcon.Request, resp: falcon.Response):
        if not rot_dev.connected:
            resp.text = PropertyResponse(None, req, 
                            NotConnectedException()).json
            return
        try:
            # ---------------------
            rev = rot_dev.step_size
            # ---------------------
        except Exception as ex:
            resp.text = PropertyResponse(None, req, 
                            DriverException(0x500, f'{self.__class__.__name__} failed', ex)).json
            return
        resp.text = PropertyResponse(rev, req).json

class TargetPosition:
    def on_get(self, req: falcon.Request, resp: falcon.Response):
        if not rot_dev.connected:
            resp.text = PropertyResponse(None, req, 
                            NotConnectedException()).json
            return
        try:
            # ---------------------------
            rev = rot_dev.target_position
            # ---------------------------
        except Exception as ex:
            resp.text = PropertyResponse(None, req, 
                            DriverException(0x500, f'{self.__class__.__name__} failed', ex)).json
            return
        resp.text = PropertyResponse(rev, req).json

class Halt:
    def on_put(self, req: falcon.Request, resp: falcon.Response):
        formdata = req.get_media()
        if not rot_dev.connected:
            resp.text = MethodResponse(formdata, 
                            NotConnectedException()).json
            return
        try:
            # ------------
            rot_dev.Halt()
            # ------------
        except Exception as ex:
            resp.text = MethodResponse(formdata, 
                            DriverException(0x500, f'{self.__class__.__name__} failed', ex)).json
            return
        resp.text = MethodResponse(formdata).json


class Move:
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
        print (f'Move({newpos}) from ClientID={formdata["ClientID"]}')
        try:
            # ------------------
            rot_dev.Move(newpos)    # async
            # ------------------
        except Exception as ex:
            resp.text = MethodResponse(formdata, 
                            DriverException(0x500, f'{self.__class__.__name__} failed', ex)).json
            return
        resp.text = MethodResponse(formdata).json

class MoveAbsolute:
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
            resp.text = MethodResponse(formdata,
                            DriverException(0x500, f'{self.__class__.__name__} failed', ex)).json
            return
        resp.text = MethodResponse(formdata).json

class MoveMechanical:
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
        print (f'MoveMechanical({newpos}) from ClientID={formdata["ClientID"]}')
        try:
            # --------------------------
            rot_dev.MoveAbsolute(newpos)    # async
            # --------------------------
        except Exception as ex:
            resp.text = MethodResponse(formdata,
                            DriverException(0x500, f'{self.__class__.__name__} failed', ex)).json
            return
        resp.text = MethodResponse(formdata).json

class Sync:
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
        print (f'Sync({newpos}) from ClientID={formdata["ClientID"]}')
        try:
            # ------------------
            rot_dev.Sync(newpos) 
            # ------------------
        except Exception as ex:
            resp.text = MethodResponse(formdata,
                            DriverException(0x500, f'{self.__class__.__name__} failed', ex)).json
            return
        resp.text = MethodResponse(formdata).json
