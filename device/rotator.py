# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# rotator.py - Endpoints for members of ASCOM Alpaca Rotator Device
#
# Part of the AlpycaDevice Alpaca skeleton/template device driver
#
# Author:   Robert B. Denny <rdenny@dc3.com> (rbd)
#
# Implements: ASCOM IRotatorV4 interface
#             https://ascom-standards.org/newdocs/rotator.html#Rotator
# Python Compatibility: Requires Python 3.7 or later
# GitHub: https://github.com/ASCOMInitiative/AlpycaDevice
#
# -----------------------------------------------------------------------------
# MIT License
#
# Copyright (c) 2022-2024 Bob Denny
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
#               and module header.
# 30-Dec-2022   rbd 0.1 Revamp request pre-processing, logging, and
#               quality control. Device number from URI.
# 31-Dec-2022   rbd 0.1 Bad boolean values return 400 Bad Request
# 15-Jan-2023   rbd 0.1 Documentation. No logic changes.
# 20-Jan-2023   rbd 0.1 Refactor for clarity
# 23-May-2023   rbd 0.2 Refactoring for  multiple ASCOM device type support
#               GitHub issue #1
# 30-May-2023   rbd 0.2 Remove redundant logging from PUT responders
# 31-May-2023   rbd 0.3 responder class names lower cased to match URI
# 08-Nov-2023   rbd 0.4 Replace exotic 'dunder' construction of error
#               messages with actual text. Just a clarification. Remove
#               superfluous () on class declarations.
# 15-Feb-2024   rbd 0.6 Upgrade to Rotator V4 (Platform 7)
# 16-Feb-2024   rbd 0.6 Passes Validtion and Protocol ConformU 2.1.0
# 20-Feb-2024   rbd 0.7 Wow. Load device from Config (and toml) ha ha.
#               Add setting for sync/async Connected write.
#
import datetime, json
from falcon import Request, Response, HTTPBadRequest, before
from logging import Logger
from shr import PropertyResponse, MethodResponse, PreProcessRequest, \
                StateValue, get_request_field, to_bool
from exceptions import *        # Nothing but exception classes
from rotatordevice import RotatorDevice

logger: Logger = None           # Really should use Pyton 3.10 or later
#logger = None                  # Safe on Python 3.7 but no intellisense in VSCode etc.

# ----------------------
# MULTI-INSTANCE SUPPORT
# ----------------------
# If this is > 0 then it means that multiple devices of this type are supported.
# Each responder on_get() and on_put() is called with a devnum parameter to indicate
# which instance of the device (0-based) is being called by the client. Leave this
# set to 0 for the simple case of controlling only one instance of this device type.
#
maxdev = 0                      # Single instance

# -------------------
# ROTATOR DEVICE INFO
# -------------------
# Static metadata not subject to configuration changes
class RotatorMetadata:
    """ Metadata describing the Rotator Device. Edit for your device"""
    Name = 'Sample Rotator'
    Version = '0.6'
    Description = 'Sample ASCOM Rotator'
    DeviceType = 'Rotator'
    DeviceID = '1892ED30-92F3-4236-843E-DA8EEEF2D1CC' # https://guidgenerator.com/online-guid-generator.aspx
    Info = 'Alpaca Sample Device\nImplements IRotatorV4\nASCOM Initiative'
    MaxDeviceNumber = maxdev
    InterfaceVersion = 4        # IRotatorV4 (Platform 7)

# --------------------
# SIMULATED ROTATOR ()
# --------------------
rot_dev = None
# At app init not import :-)
def start_rot_device(logger: logger):
    logger = logger
    global rot_dev
    rot_dev = RotatorDevice(logger)
    rot_dev.can_reverse = Config.can_reverse
    rot_dev.step_size = Config.step_size
    rot_dev.steps_per_sec = Config.steps_per_sec
    rot_dev.sync_write_connected = Config.sync_write_connected

# --------------------
# RESOURCE CONTROLLERS
# --------------------
@before(PreProcessRequest(maxdev))
class action:
    """Invoke the specified device-specific custom action

        See https://ascom-standards.org/newdocs/rotator.html#Rotator.Action
    """
    def on_put(self, req: Request, resp: Response, devnum: int):
        name = get_request_field('ActionName', req)
        params = get_request_field('ActionParameters', req)
        # See SupportedActions
        # Python 3.10 or newer
        match name.lower():
            case 'myaction':
                logger.info('MyAction called')
                # Execute rot_dev.MyAction(params)
            case 'youraction':
                logger.info('YourAction called')
                # Execute rot_dev.YourAction(params)
            case _:
                resp.text = MethodResponse(req, ActionNotImplementedException())
        # If you don't want to implement this at all then
        # resp.text = MethodResponse(req, NotImplementedException()).json

@before(PreProcessRequest(maxdev))
class commandblind:
    # Do not use
    def on_put(self, req: Request, resp: Response, devnum: int):
        resp.text = MethodResponse(req, NotImplementedException()).json

@before(PreProcessRequest(maxdev))
class commandbool:
    # Do not use
    def on_put(self, req: Request, resp: Response, devnum: int):
        resp.text = MethodResponse(req, NotImplementedException()).json

@before(PreProcessRequest(maxdev))
class commandstring:
    # Do not use
    def on_put(self, req: Request, resp: Response, devnum: int):
        resp.text = MethodResponse(req, NotImplementedException()).json

# Connected, though common, is implemented in rotator.py
@before(PreProcessRequest(maxdev))
class description:
    """Description of the device such as manufacturer and model number.
        Any ASCII characters may be used.

        See https://ascom-standards.org/newdocs/rotator.html#Rotator.Description
    """
    def on_get(self, req: Request, resp: Response, devnum: int):
        resp.text = PropertyResponse(RotatorMetadata.Description, req).json

@before(PreProcessRequest(maxdev))
class driverinfo:
    """Descriptive and version information about the ASCOM **driver**

        See https://ascom-standards.org/newdocs/rotator.html#Rotator.DriverInfo
    """
    def on_get(self, req: Request, resp: Response, devnum: int):
        resp.text = PropertyResponse(RotatorMetadata.Info, req).json

@before(PreProcessRequest(maxdev))
class interfaceversion:
    """ASCOM Device interface definition version that this device supports.
        Should return 4 for this interface version IRotatorV4.

        See https://ascom-standards.org/newdocs/rotator.html#Rotator.InterfaceVersion
    """
    def on_get(self, req: Request, resp: Response, devnum: int):
        resp.text = PropertyResponse(RotatorMetadata.InterfaceVersion, req).json

@before(PreProcessRequest(maxdev))
class driverversion:
    """String containing only the major and minor version of the **driver**.

        See https://ascom-standards.org/newdocs/rotator.html#Rotator.DriverVersion
    """
    def on_get(self, req: Request, resp: Response, devnum: int):
        resp.text = PropertyResponse(RotatorMetadata.Version, req).json

@before(PreProcessRequest(maxdev))
class name:
    """The short name of the **driver**, for display purposes.

        See https://ascom-standards.org/newdocs/rotator.html#Rotator.Name
    """
    def on_get(self, req: Request, resp: Response, devnum: int):
        resp.text = PropertyResponse(RotatorMetadata.Name, req).json

@before(PreProcessRequest(maxdev))
class supportedactions:
    """Returns the list of custom action names, to be used with ``Action()``,
        supported by this driver.

        See https://ascom-standards.org/newdocs/rotator.html#Rotator.SupportedActions
    """
    def on_get(self, req: Request, resp: Response, devnum: int):
        val = []
        val.append('MyAction')
        val.append('YourAction')
        resp.text = PropertyResponse(val, req).json  # Not PropertyNotImplemented

@before(PreProcessRequest(maxdev))
class canreverse:
    """True if the rotator supports the ``Reverse`` method

        Seehttps://ascom-standards.org/newdocs/rotator.html#Rotator.CanReverse

        Always True for IRotatorV3 (InterfaceVersion >= 3).
    """
    def on_get(self, req: Request, resp: Response, devnum: int):
        resp.text = PropertyResponse(True, req).json    # IRotatorV3, CanReverse must be True

@before(PreProcessRequest(maxdev))
class connect:
    """Connect to the device asynchronously

        See https://ascom-standards.org/newdocs/rotator.html#Rotator.Connect
    """
    def on_put(self, req: Request, resp: Response, devnum: int):
        try:
            rot_dev.Connect()
            resp.text = MethodResponse(req).json
        except Exception as ex:
            resp.text = MethodResponse(req,
                            DriverException(0x500, 'Rotator.Connect failed', ex)).json

@before(PreProcessRequest(maxdev))
class connected:
    """Retrieves or sets the connected state of the device

        See https://ascom-standards.org/newdocs/rotator.html#Rotator.Connected

        Notes:
            There is a setting ``sync_write_connected`` in config.toml that
            determines whether connecting by writing ``Connected = True`` behaves
            synchronously or acts asynchronously. Conform requires this to be synchronous
            per IRotatorV3 (PLatform 6).
    """
    def on_get(self, req: Request, resp: Response, devnum: int):
        resp.text = PropertyResponse(rot_dev.connected, req).json

    def on_put(self, req: Request, resp: Response, devnum: int):
        conn_str = get_request_field('Connected', req)
        conn = to_bool(conn_str)              # Raises 400 Bad Request if str to bool fails

        try:
            # ----------------------
            rot_dev.connected = conn
            # ----------------------
            resp.text = MethodResponse(req).json
        except Exception as ex:
            resp.text = MethodResponse(req, # Put is actually like a method :-(
                            DriverException(0x500, 'Rotator.Connected failed', ex)).json

@before(PreProcessRequest(maxdev))
class connecting:
    """True while the device is undertaking an asynchronous connect or disconnect operation.

        See https://ascom-standards.org/newdocs/rotator.html#Rotator.Connecting
    """
    def on_get(self, req: Request, resp: Response, devnum: int):
        try:
            val = rot_dev.connecting
            resp.text = PropertyResponse(val, req).json
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                            DriverException(0x500, 'Rotator.Connecting failed', ex)).json

@before(PreProcessRequest(maxdev))
class devicestate:
    """List of StateValue objects representing the operational properties of this device.

        See https://ascom-standards.org/newdocs/rotator.html#Rotator.DeviceState
    """
    def on_get(self, req: Request, resp: Response, devnum: int):
        if not rot_dev.connected:
            resp.text = PropertyResponse(None, req,
                            NotConnectedException()).json
            return
        try:
            val = []
            val.append(StateValue('IsMoving', rot_dev.is_moving))
            val.append(StateValue('MechanicalPosition', rot_dev.mechanical_position))
            val.append(StateValue('Position', rot_dev.position))
            val.append(StateValue('TimeStamp', datetime.datetime.utcnow().isoformat()))
            resp.text = PropertyResponse(val, req).json
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                            DriverException(0x500, 'Camera.Devicestate failed', ex)).json

@before(PreProcessRequest(maxdev))
class disconnect:
    """Disconnect from the device asynchronously.

        See https://ascom-standards.org/newdocs/rotator.html#Rotator.Disconnect

        NOTE: In this sample, Disconnect is instantaneous
    """
    def on_put(self, req: Request, resp: Response, devnum: int):
        try:
            rot_dev.Disconnect()
            resp.text = MethodResponse(req).json
        except Exception as ex:
            resp.text = MethodResponse(req,
                            DriverException(0x500, 'Rotator.Disconnect failed', ex)).json

@before(PreProcessRequest(maxdev))
class ismoving:
    """True if the rotator is currently moving to a new angle

        See https://ascom-standards.org/newdocs/rotator.html#Rotator.IsMoving
    """
    def on_get(self, req: Request, resp: Response, devnum: int):
        if not rot_dev.connected:
            resp.text = PropertyResponse(None, req,
                            NotConnectedException()).json
            return
        try:
            # ---------------------
            moving = rot_dev.is_moving
            # ---------------------
            resp.text = PropertyResponse(moving, req).json
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                            DriverException(0x500, 'Rotator.IsMovingfailed', ex)).json

@before(PreProcessRequest(maxdev))
class mechanicalposition:
    """The raw mechanical position of the rotator in degrees.

        See https://ascom-standards.org/newdocs/rotator.html#Rotator.MechanicalPosition
    """
    def on_get(self, req: Request, resp: Response, devnum: int):
        if not rot_dev.connected:
            resp.text = PropertyResponse(None, req,
                            NotConnectedException()).json
            return
        try:
            # -------------------------------
            pos = rot_dev.mechanical_position
            # -------------------------------
            resp.text = PropertyResponse(pos, req).json
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                            DriverException(0x500, 'Rotator.MechanicalPosition failed', ex)).json

@before(PreProcessRequest(maxdev))
class position:
    """Current instantaneous Rotator position, allowing for any sync offset, in degrees.

        See https://ascom-standards.org/newdocs/rotator.html#Rotator.Position
    """
    def on_get(self, req: Request, resp: Response, devnum: int):
        if not rot_dev.connected:
            resp.text = PropertyResponse(None, req,
                            NotConnectedException()).json
            return
        try:
            # -------------------------------
            pos = rot_dev.position
            # -------------------------------
            resp.text = PropertyResponse(pos, req).json
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                            DriverException(0x500, 'Rotator.Position failed', ex)).json

@before(PreProcessRequest(maxdev))
class reverse:
    """The direction of rotation CCW or CW

        See https://ascom-standards.org/newdocs/rotator.html#Rotator.Reverse
    """
    def on_get(self, req: Request, resp: Response, devnum: int):
        if not rot_dev.connected:
            resp.text = PropertyResponse(None, req,
                            NotConnectedException()).json
            return
        try:
            # -------------------
            rev = rot_dev.reverse
            # -------------------
            resp.text = PropertyResponse(rev, req).json
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                            DriverException(0x500, 'Rotator.Reverse failed', ex)).json

    def on_put(self, req: Request, resp: Response, devnum: int):
        if not rot_dev.connected:
            resp.text = MethodResponse(req,
                            NotConnectedException()).json
            return
        rev_str = get_request_field('Reverse', req)
        rev = to_bool(rev_str)              # Raises 400 Bad Request if str to bool fails
        try:
            # ----------------------
            rot_dev.reverse = rev
            # ----------------------
            resp.text = MethodResponse(req).json
        except Exception as ex:
            resp.text = MethodResponse(req, # Put is actually like a method :-(
                            DriverException(0x500, 'Rotator.Reverse failed', ex)).json

@before(PreProcessRequest(maxdev))
class stepsize:
    """Minimum rotation step size (deg)

        See https://ascom-standards.org/newdocs/rotator.html#Rotator.StepSize
    """
    def on_get(self, req: Request, resp: Response, devnum: int):
        if not rot_dev.connected:
            resp.text = PropertyResponse(None, req,
                            NotConnectedException()).json
            return
        try:
            # ---------------------
            steps = rot_dev.step_size
            # ---------------------
            resp.text = PropertyResponse(steps, req).json
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                            DriverException(0x500, 'Rotator.StepSize failed', ex)).json

@before(PreProcessRequest(maxdev))
class targetposition:
    """The destination angle for ``Move()`` and ``MoveAbsolute()``

        See https://ascom-standards.org/newdocs/rotator.html#Rotator.TargetPosition
    """
    def on_get(self, req: Request, resp: Response, devnum: int):
        if not rot_dev.connected:
            resp.text = PropertyResponse(None, req,
                            NotConnectedException()).json
            return
        try:
            # ---------------------------
            pos = rot_dev.target_position
            # ---------------------------
            resp.text = PropertyResponse(pos, req).json
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                            DriverException(0x500, 'Rotator.TargetPosition failed', ex)).json

@before(PreProcessRequest(maxdev))
class halt:
    """Immediately stop any rotator motion

        See https://ascom-standards.org/newdocs/rotator.html#Rotator.Halt
    """
    def on_put(self, req: Request, resp: Response, devnum: int):
        if not rot_dev.connected:
            resp.text = MethodResponse(req,
                            NotConnectedException()).json
            return
        try:
            # ------------
            rot_dev.Halt()
            # ------------
            resp.text = MethodResponse(req).json
        except Exception as ex:
            resp.text = MethodResponse(req,
                            DriverException(0x500, 'Rotator.Halt failed', ex)).json


@before(PreProcessRequest(maxdev))
class move:
    """Start rotation relative to the current position (degrees)

        See https://ascom-standards.org/newdocs/rotator.html#Rotator.Move
    """
    def on_put(self, req: Request, resp: Response, devnum: int):
        if not rot_dev.connected:
            resp.text = MethodResponse(req,
                            NotConnectedException()).json
            return
        pos_str = get_request_field('Position', req)    # May raise 400 bad request
        try:
            newpos = origpos = float(pos_str)
        except:
            resp.text = MethodResponse(req,
                            InvalidValueException(f'Position {pos_str} not a valid integer.')).json
            return
        # The spec calls for "anything goes" requires you to range the
        # final value modulo 360 degrees.
        if newpos >= 360.0:
            newpos -= 360.0
            logger.debug('Result would be >= 360, setting to {newpos}')
        if newpos < 0:
            newpos += 360
            logger.debug('Result would be < 0, setting to {newpos}')
        try:
            # ------------------
            rot_dev.Move(newpos)    # async
            # ------------------
            resp.text = MethodResponse(req).json
        except Exception as ex:
            resp.text = MethodResponse(req,
                            DriverException(0x500, 'Rotator.Move failed', ex)).json

@before(PreProcessRequest(maxdev))
class moveabsolute:
    """Start rotation to the given ``Position`` (degrees)

        See https://ascom-standards.org/newdocs/rotator.html#Rotator.MoveAbsolute
    """
    def on_put(self, req: Request, resp: Response, devnum: int):
        if not rot_dev.connected:
            resp.text = MethodResponse(req,
                            NotConnectedException()).json
            return
        pos_str = get_request_field('Position', req)
        try:
            newpos = float(pos_str)
        except:
            resp.text = MethodResponse(req,
                            InvalidValueException(f'Position {pos_str} not a valid integer.')).json
            return
        if newpos < 0.0 or newpos >= 360.0:
            resp.text = MethodResponse(req,
                            InvalidValueException(f'Invalid position {str(newpos)} outside range 0 <= pos < 360.')).json
            return
        try:
            # --------------------------
            rot_dev.MoveAbsolute(newpos)    # async
            # --------------------------
            resp.text = MethodResponse(req).json
        except Exception as ex:
            resp.text = MethodResponse(req,
                            DriverException(0x500, 'Rotator.MoveAbsolute failed', ex)).json

@before(PreProcessRequest(maxdev))
class movemechanical:
    """Start rotation to the given new mechanical position (degrees)

    See https://ascom-standards.org/newdocs/rotator.html#Rotator.MoveMechanical
    """
    def on_put(self, req: Request, resp: Response, devnum: int):
        formdata = req.get_media()
        if not rot_dev.connected:
            resp.text = MethodResponse(req,
                            NotConnectedException()).json
            return
        pos_str = get_request_field('Position', req)
        try:
            newpos = float(pos_str)
        except:
            resp.text = MethodResponse(req,
                            InvalidValueException(f'Position {formdata["Position"]} not a valid integer.')).json
            return
        if newpos < 0.0 or newpos >= 360.0:
            resp.text = MethodResponse(req,
                            InvalidValueException(f'Invalid position {str(newpos)} outside range 0 <= pos < 360.')).json
            return
        try:
            # ----------------------------
            rot_dev.MoveMechanical(newpos)    # async
            # ----------------------------
            resp.text = MethodResponse(req).json
        except Exception as ex:
            resp.text = MethodResponse(req,
                            DriverException(0x500, 'Rotator.MoveMechanical failed', ex)).json

@before(PreProcessRequest(maxdev))
class sync:
    """Syncs the rotator to the specified position angle (degrees) without moving it.

        See https://ascom-standards.org/newdocs/rotator.html#Rotator.Sync
    """
    def on_put(self, req: Request, resp: Response, devnum: int):
        formdata = req.get_media()
        if not rot_dev.connected:
            resp.text = MethodResponse(req,
                            NotConnectedException()).json
            return
        pos_str = get_request_field('Position', req)
        try:
            newpos = float(pos_str)
        except:
            resp.text = MethodResponse(req,
                            InvalidValueException(f'Position {formdata["Position"]} not a valid integer.')).json
            return
        if newpos < 0.0 or newpos >= 360.0:
            resp.text = MethodResponse(req,
                            InvalidValueException(f'Invalid position {str(newpos)} outside range 0 <= pos < 360.')).json
            return
        try:
            # ------------------
            rot_dev.Sync(newpos)
            # ------------------
            resp.text = MethodResponse(req).json
        except Exception as ex:
            resp.text = MethodResponse(req,
                            DriverException(0x500, 'Rotator.Sync failed', ex)).json
