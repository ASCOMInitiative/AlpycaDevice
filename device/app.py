#
# 16-Dec-2022   rbd 1.0 Initial edit for Alpaca sample/template
#

from wsgiref.simple_server import make_server
import os
import inspect
import falcon
# Controller classes (for routing)
import common
import rotator
import management

API_VERSION = 1

# -------------------
# Discovery responder
# -------------------
from discovery import DiscoveryResponder

# -----------------
# Network Connection
# ----------------
if os.name == 'nt':                                     # This is really Windows (my dev system eh?)
    HOST = '127.0.0.1'
    MCAST = '127.0.0.255'
    print(f' * Running on Windows for Development... {HOST}')
    print(f' * Assuming broadcast address is {MCAST}')
else:
#
# Unbelievable what you need to do to get your live IP address
# on Linux (which one????) and even more fun to know the 
# correct multicast address. This is a sample so I just hard code
# both here. See ipsddress and netifaces if you want some fun.
#
    HOST = '192.168.0.42'                               # Your device's IP(V4) address
    MCAST = '192.168.0.255'                             # Discovery: Depends on your CIDR block
    print(f' * Assuming run on Raspberry Pi Linux {HOST}')

PORT = 5555                                             # Port on which the device responds

# ---------
# DISCOVERY
# ---------
_DSC = DiscoveryResponder(MCAST, HOST, PORT)

# ----------------------------------
# MAIN HTTP/REST API ENGINE (FALCON)
# ----------------------------------
# falcon.App instances are callable WSGI apps
falc_app = falcon.App()
#
# Initialize routes for each endpoint the magic way
#
def init_routes(app: falcon.App, module):
    # Magic to get list of endpoint controller classes in given module
    # Note that it is suufficient to create the controller instance
    # directly from the type returned by inspect.getmembers since 
    # the instance is saved within Falcon as its resource controller.
    memlist = inspect.getmembers(module, inspect.isclass)
    for cname,ctype in memlist:
        if ctype.__module__ == module.__name__:    # Only classes *defined* in the module
            app.add_route(f'/api/v{API_VERSION}/{cname.lower()}', ctype())  # type() creates instance!
init_routes(falc_app, common)
init_routes(falc_app, rotator)                          # TODO FOR YOUR DEVICE TYPE
falc_app.add_route('/management/apiversions', management.apiversions())
falc_app.add_route(f'/management/v{API_VERSION}/description', management.description())
falc_app.add_route(f'/management/v{API_VERSION}/configureddevices', management.configureddevices())


# ==================
# SERVER APPLICATION
# ==================

if __name__ == '__main__':
    # Using the lightweight built-in Python wsgi.simple_server
    with make_server(HOST, PORT, falc_app) as httpd:
        print(f'Serving on port {PORT}...')

        # Serve until process is killed
        httpd.serve_forever()

