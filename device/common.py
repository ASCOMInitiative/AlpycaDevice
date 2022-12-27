# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# common.py - Endpoints for members common to all Alpaca devices
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
# 18-Dec-2022   rbd 0.1 Implement remaining controller classes
# 20-Dec-2022   rbd 0.1 Fix SupportedActions ha ha.
# 22-Dec-2022   rbd 0.1 Refectored metadata support
# 24-Dec-2022   rbd 0.1 Logging
# 25-Dec-2022   rbd 0.1 Logging typing for intellisense
# 26-Dec-2022   rbd 0.1 Logging of endpoints
# 27-Dec-2022   rbd 0.1 Revamp logging so request precedes response.
#               Minimize imported stuff. MIT license and module header.
#
from falcon import Request, Response
from exceptions import *    # Only exception classes here
from shr import PropertyResponse, MethodResponse, DeviceMetadata, log_request
from logging import Logger

logger: Logger = None   # Set to global logger at app startup

# --------------------
# RESOURCE CONTROLLERS
# --------------------

class Action:
    def on_put(self, req: Request, resp: Response):
        log_request(req)
        resp.text = MethodResponse(req, NotImplementedException()).json

class CommandBlind:
    def on_put(self, req: Request, resp: Response):
        log_request(req)
        resp.text = MethodResponse(req, NotImplementedException()).json

class CommandBool:
    def on_put(self, req: Request, resp: Response):
        log_request(req)
        logger.info(f'{req.remote_addr} {req.media}')
        resp.text = MethodResponse(req, NotImplementedException()).json

class CommandString():
    def on_put(self, req: Request, resp: Response):
        log_request(req)
        resp.text = MethodResponse(req, NotImplementedException()).json

# Connected, though common, is implemented in rotator.py
class Description():
    def on_get(self, req: Request, resp: Response):
        log_request(req)
        resp.text = PropertyResponse(DeviceMetadata.Description, req).json

class DriverInfo():
    def on_get(self, req: Request, resp: Response):
        log_request(req)
        resp.text = PropertyResponse(DeviceMetadata.Info, req).json

class InterfaceVersion():
    def on_get(self, req: Request, resp: Response):
        log_request(req)
        resp.text = PropertyResponse(DeviceMetadata.InterfaceVersion, req).json

class DriverVersion():
    def on_get(self, req: Request, resp: Response):
        log_request(req)
        resp.text = PropertyResponse(DeviceMetadata.Version, req).json

class Name():
    def on_get(self, req: Request, resp: Response):
        log_request(req)
        resp.text = PropertyResponse(DeviceMetadata.Name, req).json

class SupportedActions():
    def on_get(self, req: Request, resp: Response):
        log_request(req)
        resp.text = PropertyResponse([], req).json  # Not PropertyNotImplemented

