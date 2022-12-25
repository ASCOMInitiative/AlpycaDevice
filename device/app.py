#
# 16-Dec-2022   rbd 0.1 Initial edit for Alpaca sample/template
# 20-Dec-2022   rbd 0.1 Correct endpoint URIs
# 21-Dec-2022   rbd 0.1 Refactor for import protection. Add configurtion.
# 22-Dec-2020   rbd 0.1 Start of logging 
# 24-Dec-2022   rbd 0.1 Logging
# 25-Dec-2022   rbd 0.1 Add milliseconds to logger time stamp
#
from wsgiref.simple_server import  WSGIRequestHandler, make_server
import sys
import inspect
import time
import falcon
import logging.handlers
# Controller classes (for routing)
import common
import rotator
import management
# Config file support
from conf import Config
# Discovery module
from discovery import DiscoveryResponder, set_disc_logger
# Just the shared logger hooks avoid importing other stuff
#from conf import set_conf_logger
from shr import set_shr_logger

global logger
logger = None               # Logger used throughout.

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
        logger.info(f'{self.client_address[0]} {format%args}')

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


    # -------
    # LOGGING
    #--------
    # This single logger is used throughout. The module name (the param for get_logger())
    # isn't needed and would be 'root' anyway, sort of useless. Also the default date-time
    # is local time, and not ISO-8601. We log in UTC/ISO format, and with fractional seconds.
    # Finally our config options allow for suppression of logging to stdout, and for this 
    # we remove the default stdout handler. Thank heaven that Python logging is thread-safe! 
    #
    global logger
    logging.basicConfig(level=Config.log_level)
    logger = logging.getLogger()                # Nameless, see above
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
        logger.debug('Logging to stdout disabled in settings')
        logger.removeHandler(logger.handlers[0])    # This is the stdout handler
    # Share this logger throughout
    common.logger = logger
    rotator.logger = logger
    rotator.start_rot_device(logger)
    set_shr_logger(logger)
    set_disc_logger(logger)
#    LoggingWSGIRequestHandler.logger = logger

    # ---------
    # DISCOVERY
    # ---------
    _DSC = DiscoveryResponder(Config.mc_address, Config.ip_address, Config.port)

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
