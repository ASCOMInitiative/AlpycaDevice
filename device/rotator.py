# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# rotator.py - Endpoints for members of ASCOM Alpaca Rotator Device
#
# Part of the AlpycaDevice Alpaca skeleton/template device driver
#
# Author:   Robert B. Denny <rdenny@dc3.com> (rbd)
#
# Python Compatibility: Requires Python 3.7 or later
# GitHub: https://github.com/ASCOMInitiative/AlpycaDevice
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
#               and module header.
# 30-Dec-2022   rbd 0.1 Revamp request pre-processing, logging, and
#               quality control. Device number from URI.
# 31-Dec-2022   rbd 0.1 Bad boolean values return 400 Bad Request
# 15-Jan-2023   rbd 0.1 Documentation. No logic changes.
#
from falcon import Request, Response, HTTPBadRequest, before
from logging import Logger
from shr import PropertyResponse, MethodResponse, PreProcessRequest, \
                get_request_field, to_bool
from exceptions import *        # Nothing but exception classes
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
    """True if the rotator supports the ``Reverse`` method

    Always True for IRotatorV3 (InterfaceVersion >= 3).
    """
    def on_get(self, req: Request, resp: Response, devnum: int):
        resp.text = PropertyResponse(True, req).json    # IRotatorV3, CanReverse must be True

@before(PreProcessRequest())
class Connected:
    """Retrieves or sets the connected state of the device

    * Set True to connect to the device hardware. Set False to disconnect
      from the device hardware. Client can also read the property to check
      whether it is connected. This reports the current hardware state.
    * Multiple calls setting Connected to true or false must not cause
      an error.

    """
    def on_get(self, req: Request, resp: Response, devnum: int):
        resp.text = PropertyResponse(rot_dev.connected, req).json

    def on_put(self, req: Request, resp: Response, devnum: int):
        formdata = req.get_media()
        conn = to_bool(formdata['Connected'])   # Raises 400 BadRequest
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
    """True if the rotator is currently moving to a new angle

    Caution:
        This must be true **immediately after** a return from calling
        ``Move()``, ``MoveAbsolute()``, or ``MoveMechanical()`` *unless*
        it is already at the requested position and is therefore not moving.
        There must
        be no possibility of seeing ``IsMoving = False`` even for an instant
        after the app calls one of the (asynchronous) Move methods with
        a *new* position. A driver must hide internal device states.

    Raises:
        NotConnectedException
            if device not connected
        DriverException
            see :ref:`driver-exception`
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
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                            DriverException(0x500, f'{self.__class__.__name__} failed', ex)).json
            return
        resp.text = PropertyResponse(moving, req).json

@before(PreProcessRequest())
class MechanicalPosition:
    """The raw mechanical position (deg) of the rotator

    Raises:
        NotConnectedException
            if device not connected
        DriverException
            see :ref:`driver-exception`

    * Value is in degrees counterclockwise from the rotator's mechanical index.
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
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                            DriverException(0x500, f'{self.__class__.__name__} failed', ex)).json
            return
        resp.text = PropertyResponse(pos, req).json

@before(PreProcessRequest())
class Position:
    """The virtual position (deg) of the rotator

    Raises:
        NotConnectedException
            if device not connected
        DriverException
            see :ref:`driver-exception`

    * Value is in degrees counterclockwise from the rotator's virtual index.
    * This angle includes offset between the mechanical index and the
      effect of the last ``Sync()``

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
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                            DriverException(0x500, f'{self.__class__.__name__} failed', ex)).json
            return
        resp.text = PropertyResponse(pos, req).json

@before(PreProcessRequest())
class Reverse:
    """The direction of rotation CCW or CW

    Raises:
        NotConnectedException
            if device not connected
        DriverException
            see :ref:`driver-exception`

    * Rotation is normally in degrees counterclockwise as viewed
      from behind the rotator, looking toward the sky. This corresponds
      to the direction of equatorial position angle. Set this property True
      to cause rotation opposite to equatorial PositionAngle, i.e. clockwise.

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
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                            DriverException(0x500, f'{self.__class__.__name__} failed', ex)).json
            return
        resp.text = PropertyResponse(rev, req).json

    def on_put(self, req: Request, resp: Response, devnum: int):
        formdata = req.get_media()
        if not rot_dev.connected:
            resp.text = MethodResponse(req,
                            NotConnectedException()).json
            return
        rev = to_bool(formdata['Reverse'])   # Raises 400 BadRequest
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
    """Minimum rotation step size (deg)

    Raises:
        NotConnectedException
            if device not connected
        NotImplementedException
            if this is not available
        DriverException
            see :ref:`driver-exception`

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
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                            DriverException(0x500, f'{self.__class__.__name__} failed', ex)).json
            return
        resp.text = PropertyResponse(steps, req).json

@before(PreProcessRequest())
class TargetPosition:
    """The destination angle for ``Move()`` and ``MoveAbsolute()``

    Raises:
        NotConnectedException
            if device not connected
        DriverException
            see :ref:`driver-exception`

    * This must contain the new Position, including any ``Sync()``
      offset, immediately upon return from a call to ``Move()`` or
      ``MoveAbsolute()``.

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
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                            DriverException(0x500, f'{self.__class__.__name__} failed', ex)).json
            return
        resp.text = PropertyResponse(pos, req).json

@before(PreProcessRequest())
class Halt:
    """Halt rotator motion.

    Raises:
        NotConnectedException
            if device not connected
        DriverException
            see :ref:`driver-exception`

    * Halting the rotator must not cause an error on subsequent operations.
    """
    def on_put(self, req: Request, resp: Response, devnum: int):
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
    """Start rotation relative to the current position (degrees)

    Must cause the ``TargetPosition`` property to change to the sum of the current
    virtual position and the value of the Position argument (modulo 360 degrees),
    then start rotation to ``TargetPosition``.

    **Non-blocking**: Must return immediately with ``IsMoving = True`` if
    the operation has *successfully* been started and the rotator is moving
    to a new position. If the rotator is already at the requested position
    then ``IsMoving`` may immediately return ``False``. See
    :ref:`async-intro`.

    Arguments:
        Position: The angular amount (degrees) to move relative to the
            current position.

    Raises:
        InvalidValueException
            if the Position argument is not a numeric value
        NotConnectedException
            if device not connected
        DriverException
            see :ref:`driver-exception`

    """
    def on_put(self, req: Request, resp: Response, devnum: int):
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
        # The spec calls for "anything goes" requires you to range the
        # final value modulo 360 degrees.
        logger.debug(f'Move({newpos}) from ClientID={formdata["ClientID"]}')
        if newpos >= 360.0:
            newpos -= 360.0
            logger.debug('Result would be >= 360, setting to {newpos}')
        if newpos < 0:
            newpos += 360
            logger.debug('Result would be < 0, setting to {newpos}')
        logger.info(f'Move({origpos}) -> {str(newpos)} ClientID={formdata["ClientID"]}')
        # TODO == end of fixit logic ==
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
    """Start rotation to the given new virtual position (degrees)

    Must cause the (virtual) ``TargetPosition`` property to change to the
    value of the Position argument then start rotation to ``TargetPosition``.

    **Non-blocking**: Must return immediately with ``IsMoving = True`` if
    the operation has *successfully* been started and the rotator is moving
    to a new position. If the rotator is already at the requested position
    then ``IsMoving`` may immediately return ``False``. See
    :ref:`async-intro`.

    Arguments:
        Position:
            The new virtual position, taking into account ``Sync()`` offset.

    Raises:
        InvalidValueException
            if the (virtual) Position argument is not a numeric value,
            or is outside 0 <= position < 360.
        NotConnectedException
            if device not connected
        DriverException
            see :ref:`driver-exception`

    """
    def on_put(self, req: Request, resp: Response, devnum: int):
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
    """Start rotation to the given new mechanical position (degrees)

    The Position is the mechanical angle, independent of any ``Sync()``
    offset. This method is to address requirements that need a physical
    rotation angle such as taking sky flats.

    **Non-blocking**: Must return immediately with ``IsMoving = True`` if
    the operation has *successfully* been started and the rotator is moving
    to a new position. If the rotator is already at the requested position
    then ``IsMoving`` may immediately return ``False``. See
    :ref:`async-intro`.

    Arguments:
        Position:
            The new mechanical position, ignoring any ``Sync()`` offset.

    Raises:
        InvalidValueException
            if the (virtual) Position argument is not a numeric value,
            or is outside 0 <= position < 360.
        NotConnectedException
            if device not connected
        DriverException
            see :ref:`driver-exception`

    """
    def on_put(self, req: Request, resp: Response, devnum: int):
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
    """Syncs the rotator to the specified position angle (degrees) without moving it.

    Once this method has been called and the sync offset determined, both the
    ``MoveAbsolute()`` method and the ``Position`` property must function in synced
    coordinates rather than mechanical coordinates.

    Arguments:
        Position: The requested angle, degrees.

    Raises:
        InvalidValueException
            if the (virtual) Position argument is not a numeric value,
            or is outside 0 <= position < 360.
        NotConnectedException
            if device not connected
        DriverException
            see :ref:`driver-exception`

    Note:
        The sync offset must persist across driver starts and device reboots.

    """
    def on_put(self, req: Request, resp: Response, devnum: int):
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
