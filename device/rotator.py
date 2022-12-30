# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# rotator.py - Endpoints for members of ASCOM Alpaca Rotator Device
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
# 16-Dec-2022   rbd 0.1 Initial edit for Alpaca sample/template
# 18-Dec-2022   rbd 0.1 For upgraded exception classes
# 19-Dec-2022   rbd 0.1 Implement all IRotatorV3 endpoints
# 24-Dec-2022   rbd 0.1 Logging
# 25-Dec-2022   rbd 0.1 Logging typing for intellisense
# 26-Dec-2022   rbd 0.1 Logging of endpoints 
# 27-Dec-2022   rbd 0.1 Revamp logging so request precedes 
#               response. Minimize imported stuff. MIT license
#               and m odule header.
#
from falcon import Request, Response, before
from logging import Logger
from shr import PropertyResponse, MethodResponse, PreProcessRequest, \
                get_request_field, to_bool
from exceptions import *    # Nothing but exception classes
from rotatordevice import RotatorDevice

#logger: Logger = None
logger = None                   # Safe on Python 3.7 but no intellisense in VSCode etc.

# --------------------
# SIMULATED ROTATOR ()
# --------------------
rot_dev = None
# At app init not import :-)
def start_rot_device(logger: logger):
    logger = logger
    global rot_dev
    rot_dev = RotatorDevice(logger)

# --------------------
# RESOURCE CONTROLLERS
# --------------------
@before(PreProcessRequest())
class CanReverse:
    def on_get(self, req: Request, resp: Response):
        resp.text = PropertyResponse(True, req).json    # IRotatorV3, CanReverse must be True

@before(PreProcessRequest())
class Connected:
    def on_get(self, req: Request, resp: Response):
        resp.text = PropertyResponse(rot_dev.connected, req).json

    def on_put(self, req: Request, resp: Response):
        formdata = req.get_media()
        try:
            conn = to_bool(formdata['Connected'])
        except:
            resp.text = MethodResponse(req,
                            InvalidValueException('Connected must be set to true or false')).json
            return
        try:
            # ----------------------
            rot_dev.connected = conn
            # ----------------------
        except Exception as ex:
            resp.text = MethodResponse(req, # Put is actually like a method :-(
                            DriverException(0x500, f'{self.__class__.__name__} failed', ex)).json
            return
        logger.info(f'(Connected = {conn}) from ClientID={formdata["ClientID"]}')
        resp.text = MethodResponse(req).json

@before(PreProcessRequest())
class IsMoving:
    def on_get(self, req: Request, resp: Response):
        if not rot_dev.connected:
            resp.text = PropertyResponse(None, req, 
                            NotConnectedException()).json
            return
        try:
            # ---------------------
            moving = rot_dev.is_moving
            # ---------------------
        except Exception as ex:
            resp.text = PropertyResponse(None, req, 
                            DriverException(0x500, f'{self.__class__.__name__} failed', ex)).json
            return
        resp.text = PropertyResponse(moving, req).json

@before(PreProcessRequest())
class MechanicalPosition:
    def on_get(self, req: Request, resp: Response):
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

@before(PreProcessRequest())
class Position:
    def on_get(self, req: Request, resp: Response):
        if not rot_dev.connected:
            resp.text = PropertyResponse(None, req, 
                            NotConnectedException()).json
            return
        try:
            # -------------------------------
            pos = rot_dev.position
            # -------------------------------
        except Exception as ex:
            resp.text = PropertyResponse(None, req, 
                            DriverException(0x500, f'{self.__class__.__name__} failed', ex)).json
            return
        resp.text = PropertyResponse(pos, req).json

@before(PreProcessRequest())
class Reverse:
    def on_get(self, req: Request, resp: Response):
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

    def on_put(self, req: Request, resp: Response):
        formdata = req.get_media()
        if not rot_dev.connected:
            resp.text = MethodResponse(req, 
                            NotConnectedException()).json
            return
        try:
            rev = to_bool(formdata['Reverse'])
        except:
            resp.text = MethodResponse(req, 
                            InvalidValueException('Reverse must be set to true or false')).json
            return
        try:
            # ----------------------
            rot_dev.reverse = rev
            # ----------------------
        except Exception as ex:
            resp.text = MethodResponse(req, # Put is actually like a method :-(
                            DriverException(0x500, f'{self.__class__.__name__} failed', ex)).json
            return
        logger.info(f'(reverse = {str(rev)}) from ClientID={formdata["ClientID"]}')
        resp.text = MethodResponse(req).json

@before(PreProcessRequest())
class StepSize:
    def on_get(self, req: Request, resp: Response):
        if not rot_dev.connected:
            resp.text = PropertyResponse(None, req, 
                            NotConnectedException()).json
            return
        try:
            # ---------------------
            steps = rot_dev.step_size
            # ---------------------
        except Exception as ex:
            resp.text = PropertyResponse(None, req, 
                            DriverException(0x500, f'{self.__class__.__name__} failed', ex)).json
            return
        resp.text = PropertyResponse(steps, req).json

@before(PreProcessRequest())
class TargetPosition:
    def on_get(self, req: Request, resp: Response):
        if not rot_dev.connected:
            resp.text = PropertyResponse(None, req, 
                            NotConnectedException()).json
            return
        try:
            # ---------------------------
            pos = rot_dev.target_position
            # ---------------------------
        except Exception as ex:
            resp.text = PropertyResponse(None, req, 
                            DriverException(0x500, f'{self.__class__.__name__} failed', ex)).json
            return
        resp.text = PropertyResponse(pos, req).json

@before(PreProcessRequest())
class Halt:
    def on_put(self, req: Request, resp: Response):
        if not rot_dev.connected:
            resp.text = MethodResponse(req, 
                            NotConnectedException()).json
            return
        logger.info(f'Halt() from ClientID={get_request_field("ClientID", req, "??")}')
        try:
            # ------------
            rot_dev.Halt()
            # ------------
        except Exception as ex:
            resp.text = MethodResponse(req, 
                            DriverException(0x500, f'{self.__class__.__name__} failed', ex)).json
            return
        resp.text = MethodResponse(req).json


@before(PreProcessRequest())
class Move:
    def on_put(self, req: Request, resp: Response):
        formdata = req.get_media()
        if not rot_dev.connected:
            resp.text = MethodResponse(req, 
                            NotConnectedException()).json
            return
        try:
            newpos = origpos = float(formdata['Position'])
        except:
            resp.text = MethodResponse(req, 
                            InvalidValueException(f'Position {formdata["Position"]} not a valid integer.')).json
            return
        # if newpos < 0.0 or newpos >= 360.0:
        #     resp.text = MethodResponse(req, 
        #                     InvalidValueException(f'Invalid position {str(newpos)} outside range 0 <= pos < 360.')).json
        #     return
        logger.debug(f'Move({newpos}) from ClientID={formdata["ClientID"]}')
        if newpos >= 360.0:
            newpos -= 360.0
            logger.debug('Result would be >= 360, setting to {newpos}')
        if newpos < 0:
            newpos += 360
            logger.debug('Result would be < 0, setting to {newpos}')
        logger.info(f'Move({origpos}) -> {str(newpos)} ClientID={formdata["ClientID"]}')
        try:
            # ------------------
            rot_dev.Move(newpos)    # async
            # ------------------
        except Exception as ex:
            resp.text = MethodResponse(req, 
                            DriverException(0x500, f'{self.__class__.__name__} failed', ex)).json
            return
        resp.text = MethodResponse(req).json

@before(PreProcessRequest())
class MoveAbsolute:
    def on_put(self, req: Request, resp: Response):
        formdata = req.get_media()
        if not rot_dev.connected:
            resp.text = MethodResponse(req, 
                            NotConnectedException()).json
            return
        try:
            newpos = float(formdata['Position'])
        except:
            resp.text = MethodResponse(req, 
                            InvalidValueException(f'Position {formdata["Position"]} not a valid integer.')).json
            return
        if newpos < 0.0 or newpos >= 360.0:
            resp.text = MethodResponse(req, 
                            InvalidValueException(f'Invalid position {str(newpos)} outside range 0 <= pos < 360.')).json
            return
        logger.info(f'MoveAbsolute({newpos}) from ClientID={formdata["ClientID"]}')
        try:
            # --------------------------
            rot_dev.MoveAbsolute(newpos)    # async
            # --------------------------
        except Exception as ex:
            resp.text = MethodResponse(req,
                            DriverException(0x500, f'{self.__class__.__name__} failed', ex)).json
            return
        resp.text = MethodResponse(req).json

@before(PreProcessRequest())
class MoveMechanical:
    def on_put(self, req: Request, resp: Response):
        formdata = req.get_media()
        if not rot_dev.connected:
            resp.text = MethodResponse(req, 
                            NotConnectedException()).json
            return
        try:
            newpos = float(formdata['Position'])
        except:
            resp.text = MethodResponse(req, 
                            InvalidValueException(f'Position {formdata["Position"]} not a valid integer.')).json
            return
        if newpos < 0.0 or newpos >= 360.0:
            resp.text = MethodResponse(req, 
                            InvalidValueException(f'Invalid position {str(newpos)} outside range 0 <= pos < 360.')).json
            return
        logger.info(f'MoveMechanical({newpos}) from ClientID={formdata["ClientID"]}')
        try:
            # ----------------------------
            rot_dev.MoveMechanical(newpos)    # async
            # ----------------------------
        except Exception as ex:
            resp.text = MethodResponse(req, 
                            DriverException(0x500, f'{self.__class__.__name__} failed', ex)).json
            return
        resp.text = MethodResponse(req).json

@before(PreProcessRequest())
class Sync:
    def on_put(self, req: Request, resp: Response):
        formdata = req.get_media()
        if not rot_dev.connected:
            resp.text = MethodResponse(req, 
                            NotConnectedException()).json
            return
        try:
            newpos = float(formdata['Position'])
        except:
            resp.text = MethodResponse(req, 
                            InvalidValueException(f'Position {formdata["Position"]} not a valid integer.')).json
            return
        if newpos < 0.0 or newpos >= 360.0:
            resp.text = MethodResponse(req, 
                            InvalidValueException(f'Invalid position {str(newpos)} outside range 0 <= pos < 360.')).json
            return
        logger.info(f'Sync({newpos}) from ClientID={formdata["ClientID"]}')
        try:
            # ------------------
            rot_dev.Sync(newpos) 
            # ------------------
        except Exception as ex:
            resp.text = MethodResponse(req,
                            DriverException(0x500, f'{self.__class__.__name__} failed', ex)).json
            return
        resp.text = MethodResponse(req).json
