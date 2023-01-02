# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# conf.py - Device configuration file and shared logger construction
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
# 24-Dec-2022   rbd 0.1 Logging
# 25-Dec-2022   rbd 0.1 More config items, separate logging section
# 27-Dec-2022   rbd 0.1 Move shared logger construction and global 
#               var here. MIT license and module header. No mcast.
#
import toml
import logging
import logging.handlers
import time
from os import getcwd

class Config:
    # ---------------
    # Network Section
    # ---------------
    ip_address: str
    port: int
    # --------------
    # Server Section
    # --------------
    location: str
    verbose_driver_exceptions: bool
    # --------------
    # Device Section
    # --------------
    can_reverse: bool
    step_size: float
    steps_per_sec: int
    # ---------------
    # Logging Section
    # ---------------
    log_level: int
    log_to_stdout: str
    max_size_mb: int
    num_keep_logs: int

    def init_config(path):
        _dict = toml.load(path)    # Errors here are fatal.
        global ip_address
        ip_address = _dict['network']['ip_address']
        global port
        port = _dict['network']['port']
        global location
        location = _dict['server']['location']
        global verbose_driver_exceptions
        verbose_driver_exceptions = _dict['server']['verbose_driver_exceptions']
        global can_reverse
        can_reverse = _dict['device']['can_reverse']
        global step_size
        step_size = _dict['device']['step_size']
        global steps_per_sec
        steps_per_sec = _dict['device']['steps_per_sec']
        global log_level
        log_level = logging.getLevelName(_dict['logging']['log_level'])  # Not documented but works (!!!!)
        global log_to_stdout
        log_to_stdout = _dict['logging']['log_to_stdout']
        global max_size_mb
        max_size_mb = _dict['logging']['max_size_mb']
        global num_keep_logs
        num_keep_logs = _dict['logging']['num_keep_logs']

"""
    -------------
    MASTER LOGGER
    -------------

    This single logger is used throughout. The module name (the param for get_logger())
    isn't needed and would be 'root' anyway, sort of useless. Also the default date-time
    is local time, and not ISO-8601. We log in UTC/ISO format, and with fractional seconds.
    Finally our config options allow for suppression of logging to stdout, and for this 
    we remove the default stdout handler. Thank heaven that Python logging is thread-safe! 
"""

global logger
#logger: logging.Logger = None  # Master copy (root) of the logger
logger = None                   # Safe on Python 3.7 but no intellisense in VSCode etc.

def init_logging():
    """ Create the logger - called at app startup """
    global logger
    logging.basicConfig(level=Config.log_level)
    logger = logging.getLogger()                # Root logger, see above
    formatter = logging.Formatter('%(asctime)s.%(msecs)03d %(levelname)s %(message)s', '%Y-%m-%dT%H:%M:%S')
    formatter.converter = time.gmtime           # UTC time
    logger.handlers[0].setFormatter(formatter)  # This is the stdout handler, level set above
    # Add a logfile handler, same formatter and level
    handler = logging.handlers.RotatingFileHandler('rotator.log', 
                                                    mode='w', 
                                                    delay=True,     # Prevent creation of empty logs
                                                    maxBytes=Config.max_size_mb * 1000000,
                                                    backupCount=Config.num_keep_logs)
    handler.setLevel(Config.log_level)
    handler.setFormatter(formatter)
    handler.doRollover()                                            # Always start with fresh log
    logger.addHandler(handler)
    if not Config.log_to_stdout:
        """
            This allows control of logging to stdout by simply
            removing the stdout handler from the logger's 
            handler list. It's always handler[0] as created
            by logging.basicConfig()
        """
        logger.debug('Logging to stdout disabled in settings')
        logger.removeHandler(logger.handlers[0])    # This is the stdout handler
