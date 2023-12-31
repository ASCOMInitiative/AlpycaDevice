# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# conf.py - Device configuration file and shared logger construction
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
# 24-Dec-2022   rbd 0.1 Logging
# 25-Dec-2022   rbd 0.1 More config items, separate logging section
# 27-Dec-2022   rbd 0.1 Move shared logger construction and global
#               var here. MIT license and module header. No mcast.
#
import sys
import toml
import logging

#
# This slimy hack is for Sphinx which, despite the toml.load() being
# run only once on the first import, it can't deal with _dict not being
# initialized or ?!?!?!?!? If you try to use getcwd() in the file name
# here, it will also choke Sphinx. This cost me a day.
#
_dict = {}
_dict = toml.load(f'{sys.path[0]}/config.toml')    # Errors here are fatal.
_dict2 = {}
try:
    # ltf - this file, if it exists can override or supplement definitions in the normal config.tom.
    # this facilitates putting the driver in a docker container where installation specific
    # configuration can be put in a file that isn't pulled from a repository
    _dict2 = toml.load('/alpyca/config.toml')
except:
    _dict2 = {}
    # file is optional so it's ok if it isn't there

def get_toml(sect: str, item: str):
    setting = ''
    s = None
    try:
        setting = _dict2[sect][item]
    except:
        try:
            setting = _dict[sect][item]
        except:
            setting = ''

    return setting

class Config:
    """Device configuration in ``config.toml``"""
    # ---------------
    # Network Section
    # ---------------
    ip_address: str = get_toml('network', 'ip_address')
    port: int = get_toml('network', 'port')
    # --------------
    # Server Section
    # --------------
    location: str = get_toml('server', 'location')
    verbose_driver_exceptions: bool = get_toml('server', 'verbose_driver_exceptions')
    # --------------
    # Device Section
    # --------------
    mqtt_server: str = get_toml('device', 'mqtt_server')
    mqtt_port: int = get_toml('device', 'mqtt_port') 
    mqtt_user: str = get_toml('device', 'mqtt_user')
    mqtt_password: str = get_toml('device', 'mqtt_password')
    topic_cloud_cover: str  = get_toml('device', 'topic_cloud_cover')
    topic_dew_point: str = get_toml('device', 'topic_dew_point')
    topic_event_rain: str = get_toml('device', 'topic_event_rain')
    topic_humidity: str = get_toml('device', 'topic_humidity')
    topic_pressure: str = get_toml('device', 'topic_pressure')
    topic_solar_radiation: str = get_toml('device', 'topic_solar_radiation')
    topic_sqm: str = get_toml('device', 'topic_sqm')
    topic_temperature: str = get_toml('device', 'topic_temperature')
    topic_wind_direction: str = get_toml('device', 'topic_wind_direction')
    topic_wind_gust: str = get_toml('device', 'topic_wind_gust')
    topic_wind_speed: str = get_toml('device', 'topic_wind_speed')
    # ---------------
    # Logging Section
    # ---------------
    log_level: int = logging.getLevelName(get_toml('logging', 'log_level'))  # Not documented but works (!!!!)
    log_to_stdout: str = get_toml('logging', 'log_to_stdout')
    max_size_mb: int = get_toml('logging', 'max_size_mb')
    num_keep_logs: int = get_toml('logging', 'num_keep_logs')
