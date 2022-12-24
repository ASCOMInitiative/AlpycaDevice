#
# 16-Dec-2022   rbd 0.1 Initial edit for Alpaca sample/template
# 20-Dec-2022   rbd 0.1 Correct endpoint URIs
# 21-Dec-2022   rbd 0.1 Refactor for import protection. Add configurtion.
# 22-Dec-2020   rbd 0.1 Start of logging 
#

from wsgiref.simple_server import  WSGIRequestHandler, make_server
import sys
import inspect
import falcon
import logging
# Controller classes (for routing)
import common
import rotator
import management
# Config file support
from conf import Config
# Discovery module
from discovery import DiscoveryResponder

#--------------
API_VERSION = 1
#--------------

#
# Control logging of requests to stdout as well as our own logfile
# https://stackoverflow.com/questions/31433682/control-wsgiref-simple-server-log
#
class LoggingWSGIRequestHandler(WSGIRequestHandler):

    def log_message(self, format, *args):
        """ 
            Produce a request log message in the venerable NCSA Common Log Format
            https://www.w3.org/Daemon/User/Config/Logging.html#common-logfile-format
            This is the  default format for wsgiref, but we capture it to log to a file

            Parameters:
                format      Nominally '"%s" %s %s'
                args[0]     HTTP Method and URI ("request")
                args[1]     HTTP response status code
                args[2]     HTTP response content-length
            
            Example:
                '"GET /api/v1/rotator/0/driverversion?ClientID=123&ClientTransactionID=321 HTTP/1.1" 200 108'
        """
        #TODO Log in UTC not local
        msg = "%s - - [%s] %s\n" % (self.client_address[0],
                                    self.log_date_time_string(),
                                    format%args)
        if Config.log_to_stdout:
            sys.stderr.write(msg)


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
    logging.basicConfig(level=Config.log_level)
    handler = logging.FileHandler('rotator.log', mode='w')
    handler.setLevel(Config.log_level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger = logging.getLogger(__name__)
    logger.addHandler(handler)

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
        logger.info(f'Serving on {Config.ip_address}:{Config.port}...')
        # Serve until process is killed
        httpd.serve_forever()

# ========================
if __name__ == '__main__':
    main()
# ========================
