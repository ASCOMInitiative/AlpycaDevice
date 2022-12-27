#
# 16-Dec-2022   rbd 0.1 Initial edit for Alpaca sample/template
# 20-Dec-2022   rbd 0.1 Correct endpoint URIs
# 21-Dec-2022   rbd 0.1 Refactor for import protection. Add configurtion.
# 22-Dec-2020   rbd 0.1 Start of logging 
# 24-Dec-2022   rbd 0.1 Logging
# 25-Dec-2022   rbd 0.1 Add milliseconds to logger time stamp
#
from wsgiref.simple_server import  WSGIRequestHandler, make_server
import inspect
import falcon
import conf
from conf import Config
# Controller classes (for routing)
import common
import rotator
import management
import exceptions
import discovery
from discovery import DiscoveryResponder

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
        conf.logger.info(f'{self.client_address[0]} {format%args}')

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

    conf.init_logging()
    logger = conf.logger
    # Share this logger throughout
    common.logger = logger
    rotator.logger = logger
    exceptions.logger = logger
    rotator.start_rot_device(logger)
    discovery.logger = logger
    # set_shr_logger(logger)

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
        logger.info('NOTE: logged data for a request precedes the logging of the request itself.')
        # Serve until process is killed
        httpd.serve_forever()

# ========================
if __name__ == '__main__':
    main()
# ========================
