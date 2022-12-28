# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# management.py - Management API for  ALpaca device
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
# 19-Dec-2022   rbd 0.1 Constants in shr.py
# 22-Dec-2022   rbd 0.1 Device metadata, Configuration
# 25-Dec-2022   rbd 0.1 Logging typing for intellisense
# 27-Dec-2022   rbd 0.1 Minimize imports. MIT license and module header.
#               Enhanced logging.
#
from falcon import Request, Response
from shr import PropertyResponse, DeviceMetadata
from config import Config
from logging import Logger
from shr import log_request

#logger: Logger = None
logger = None                   # Safe on Python 3.7 but no intellisense in VSCode etc.
def set_management_logger(lgr):
    global logger
    logger = lgr

# -----------
# APIVersions
# -----------
class apiversions:
    def on_get(self, req: Request, resp: Response):
        log_request(req)
        apis = [ 1 ]                            # TODO MAKE CONFIG OR GLOBAL
        resp.text = PropertyResponse(apis, req).json

# -----------
# Description
# -----------
class description:
    def on_get(self, req: Request, resp: Response):
        log_request(req)
        desc = {
            'ServerName'   : DeviceMetadata.Description,
            'Manufacturer' : DeviceMetadata.Manufacturer,
            'Version'      : DeviceMetadata.Version,
            'Location'     : Config.location
            }
        resp.text = PropertyResponse(desc, req).json

# -----------------
# ConfiguredDevices
# -----------------
class configureddevices():
    def on_get(self, req: Request, resp: Response):
        log_request(req)
        confarray = [                          # TODO ADD ONE FOR EACH DEVICE (ANY TYPE) SERVED
            {
            'DeviceName'    : DeviceMetadata.Name, 
            'DeviceType'    : DeviceMetadata.Type,
            'DeviceNumber'  : 0,
            'UniqueID'      : DeviceMetadata.ID 
            }
        ]
        resp.text = PropertyResponse(confarray, req).json
