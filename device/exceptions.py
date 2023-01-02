# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# exceptions.py - Alpaca Exception Classes
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
# 17-Dec-2022   rbd 0.1 Initial edit for Alpaca sample/template
# 18-Dec-2022   rbd 0.1 Refactor to support optional overriding
#                       error message, and support DriverException
#                       with variable error number.
# 26-Dev-2022   rbd 0.1 Logging, including Python low level exceptions
# 27-Dec-2022   rbd 0.1 MIT License and module header
#
import traceback
from config import Config
from logging import Logger

global logger
#logger: Logger = None
logger = None                   # Safe on Python 3.7 but no intellisense in VSCode etc.

class Success:
    def __init__(self):
        self.number: int = 0
        self.message: str = ''

    @property
    def Number(self) -> int:
        return self.number

    @property
    def Message(self) -> str:
        return self.message

class ActionNotImplementedException:
    def __init__(
            self, 
            message: str = 'The requested action is not implemented in this driver.'
        ):
        self.number = 0x40C
        self.message = message
        cname = self.__class__.__name__
        logger.error(f'{cname}: {message}')

    @property
    def Number(self) -> int:
        return self.number

    @property
    def Message(self) -> str:
        return self.message


# The device chooses a number between 0x500 and 0xFFF, and
# provides a helpful/specific error message. Asserts the
# error number within range.
#
# args:

class DriverException:
    """
    **Exception Class for Driver Internal Errors**
        This exception is used for device errors and other internal exceptions. 
        It can be instantiated with a captured exception object, and if so format 
        the Alpaca error message to include line number/module or optionally a 
        complete traceback of the exception (a config option).
    """
    def __init__(
            self, 
            number: int = 0x500,
            message: str = 'Internal driver error - this should be more specific.',
            exc = None  # Python exception info 
        ):
        """Initialize the DeviceException object
        
        Args:
            number (int):   Alpaca error number between 0x500 and 0xFFF, your choice
            message (str):  Specific error message or generic if left blank (see above)
            exc:            Contents 'ex' of 'except Exception as ex:' If not included
                            then only message is included. If supplied, then a detailed
                            error message with traceback is created (see full parameter)
            full (bool):    If True, a full traceback is included in the message.
                            Defaulted True above with exc_verbose, may be overriden
                            at construction time.
        """
        if number >= 0x500 and number <= 0xFFF:
            raise InvalidValueException('Programmer error, bad DriverException number')
        self.number = number
        cname = self.__class__.__name__
        if not exc is None:
            if Config.verbose_driver_exceptions:
                self.fullmsg = f'{cname}: {message}\n{traceback.format_exc()}'  # TODO Safe if not explicitly using exc?
            else:
                self.fullmsg = f'{cname}: {message}\n{type(exc).__name__}: {str(exc)}'
        else:
            self.fullmsg = f'{cname}: {message}'
        logger.error(self.fullmsg)

    @property
    def Number(self) -> int:
        return self.number

    @property
    def Message(self) -> str:
        return self.fullmsg


class InvalidOperationException:
    def __init__(
            self, 
            message: str = 'The requested operation cannot be undertaken at this time.'
        ):
        self.number = 0x40B
        self.message = message
        cname = self.__class__.__name__
        logger.error(f'{cname}: {message}')

    @property
    def Number(self) -> int:
        return self.number

    @property
    def Message(self) -> str:
        return self.message


class InvalidValueException:
    def __init__(
            self, 
            message: str = 'Invalid value given.'
        ):
        self.number = 0x401
        self.message = message
        cname = self.__class__.__name__
        logger.error(f'{cname}: {message}')

    @property
    def Number(self) -> int:
        return self.number

    @property
    def Message(self) -> str:
        return self.message


class NotConnectedException:
    def __init__(
            self, 
            message: str = 'The device is not connected.'
        ):
        self.number = 0x407
        self.message = message
        cname = self.__class__.__name__
        logger.error(f'{cname}: {message}')

    @property
    def Number(self) -> int:
        return self.number

    @property
    def Message(self) -> str:
        return self.message

class NotImplementedException:
    def __init__(
            self, 
            message: str = 'Property or method not implemented.'
        ):
        self.number = 0x400
        self.message = message
        cname = self.__class__.__name__
        logger.error(f'{cname}: {message}')

    @property
    def Number(self) -> int:
        return self.number

    @property
    def Message(self) -> str:
        return self.message

class ParkedException:
    def __init__(
            self, 
            message: str = 'Illegal operation while parked.'
        ):
        self.number = 0x408
        self.message = message
        cname = self.__class__.__name__
        logger.error(f'{cname}: {message}')

    @property
    def Number(self) -> int:
        return self.number

    @property
    def Message(self) -> str:
        return self.message

class SlavedException:
    def __init__(
            self, 
            message: str = 'Illegal operation while slaved.'
        ):
        self.number = 0x409
        self.message = message
        cname = self.__class__.__name__
        logger.error(f'{cname}: {message}')

    @property
    def Number(self) -> int:
        return self.number

    @property
    def Message(self) -> str:
        return self.message


class ValueNotSetException:
    def __init__(
            self, 
            message: str = 'The value has not yet been set.'
        ):
        self.number = 0x402
        self.message = message
        cname = self.__class__.__name__
        logger.error(f'{cname}: {message}')

    @property
    def Number(self) -> int:
        return self.number

    @property
    def Message(self) -> str:
        return self.message

