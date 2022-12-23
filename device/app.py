#
# 16-Dec-2022   rbd 0.1 Initial edit for Alpaca sample/template
# 20-Dec-2022   rbd 0.1 Correct endpoint URIs
# 21-Dec-2022   rbd 0.1 Refactor for import protection. Add configurtion.
#

from wsgiref.simple_server import make_server
import os
import inspect
import falcon
# Controller classes (for routing)
import common
import rotator
import management
# Config file support
from conf import Config

#--------------
API_VERSION = 1
#--------------

# -------------------
# Discovery responder
# -------------------
from discovery import DiscoveryResponder

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
    with make_server(Config.ip_address, Config.port, falc_app) as httpd:
        print(f'Serving on {Config.ip_address}:{Config.port}...')
        # Serve until process is killed
        httpd.serve_forever()

# ========================
if __name__ == '__main__':
    main()
# ========================
