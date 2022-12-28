# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# app.py - Application module
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
# 20-Dec-2022   rbd 0.1 Correct endpoint URIs
# 21-Dec-2022   rbd 0.1 Refactor for import protection. Add configurtion.
# 22-Dec-2020   rbd 0.1 Start of logging 
# 24-Dec-2022   rbd 0.1 Logging
# 25-Dec-2022   rbd 0.1 Add milliseconds to logger time stamp
# 27-Dec-2022   rbd 0.1 Post-processing logging of request only if not 200 OK
#               MIT License and module header. No multicast on device duh.
# 28-Dec-2022   rbd 0.1 Rename conf.py to config.py to avoid conflict with sphinx
#
import inspect
from wsgiref.simple_server import WSGIRequestHandler, make_server

# -- isort wants the above line to be blank --
# Controller classes (for routing)
import common
import config
import discovery
import exceptions
import falcon
import management
import rotator
import setup
from config import Config
from discovery import DiscoveryResponder
from shr import set_shr_logger

#--------------
API_VERSION = 1
#--------------

#
# Control logging of requests to stdout as well as our own logfile
# https://stackoverflow.com/questions/31433682/control-wsgiref-simple-server-log
#
class LoggingWSGIRequestHandler(WSGIRequestHandler):
    #logger = None           # Set during app startup
    def log_message(self, format, *args):
        """ 
            Parameters:
                format      Nominally '"%s" %s %s'
                args[0]     HTTP Method and URI ("request")
                args[1]     HTTP response status code
                args[2]     HTTP response content-length
        """
        if args[1] != '200':  # Log this only on non-200 responses
            config.logger.info(f'{self.client_address[0]} <- {format%args}')

#-----------------------
# Magic routing function
# ----------------------
def init_routes(app: falcon.App, devname: str, module):
    # Magic to get list of endpoint controller classes in given module
    # Note that it is suufficient to create the controller instance
    # directly from the type returned by inspect.getmembers since 
    # the instance is saved within Falcon as its resource controller.
    # Single device implementation, device #0
    memlist = inspect.getmembers(module, inspect.isclass)
    for cname,ctype in memlist:
        if ctype.__module__ == module.__name__:    # Only classes *defined* in the module
            app.add_route(f'/api/v{API_VERSION}/{devname}/0/{cname.lower()}', ctype())  # type() creates instance!

# ===========
# APP STARTUP 
# ===========
def main():

    config.init_logging()
    logger = config.logger
    # Share this logger throughout
    common.logger = logger
    rotator.logger = logger
    exceptions.logger = logger
    rotator.start_rot_device(logger)
    discovery.logger = logger
    set_shr_logger(logger)

    # ---------
    # DISCOVERY
    # ---------
    _DSC = DiscoveryResponder(Config.ip_address, Config.port)

    # ----------------------------------
    # MAIN HTTP/REST API ENGINE (FALCON)
    # ----------------------------------
    # falcon.App instances are callable WSGI apps
    falc_app = falcon.App()
    #
    # Initialize routes for each endpoint the magic way
    #
    init_routes(falc_app, 'rotator', common)
    init_routes(falc_app, 'rotator', rotator)
    falc_app.add_route('/management/apiversions', management.apiversions())
    falc_app.add_route(f'/management/v{API_VERSION}/description', management.description())
    falc_app.add_route(f'/management/v{API_VERSION}/configureddevices', management.configureddevices())
    falc_app.add_route('/setup', setup.svrsetup())
    falc_app.add_route(f'/setup/v{API_VERSION}/rotator/0/setup', setup.devsetup())

    # ------------------
    # SERVER APPLICATION
    # ------------------
    # Using the lightweight built-in Python wsgi.simple_server
    with make_server(Config.ip_address, Config.port, falc_app, handler_class=LoggingWSGIRequestHandler) as httpd:
        logger.info(f'==STARTUP== Serving on {Config.ip_address}:{Config.port}. Time stamps are UTC.')
        # Serve until process is killed
        httpd.serve_forever()

# ========================
if __name__ == '__main__':
    main()
# ========================
