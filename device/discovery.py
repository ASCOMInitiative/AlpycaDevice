# ====================================================
# DISCOVERY.PY - Discovery Responder for Alpaca Device
# ====================================================
#
# 17-Dec-2022   rbd 0.1 Initial edit for Alpaca sample/template
# 19-Dec-2022   rbd 0.1 Validated with ConformU discovery diagnostics
#               Add thread name 'Discovery'
# 24-Dec-2022   rbd 0.1 Logging
#
import os
import socket                                           # for discovery responder
from threading import Thread                            # Same here
import logging

global logger
logger  = None
def set_disc_logger(lgr) -> logger:
    logger = lgr

class DiscoveryResponder(Thread):
    def __init__(self, MCAST, ADDR, PORT):
        Thread.__init__(self, name='Discovery')
        # TODO See https://stackoverflow.com/a/32372627/159508
        # It's a sledge hammer technique to bind to ' ' for sending multicast
        # The right way is to bind to the broadcast address for the current
        # subnet. 
        self.device_address = (MCAST, 32227)    # Listen at multicast address, not ' '
        self.alpaca_response  = "{\"AlpacaPort\": " + str(PORT) + "}"
        self.rsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.rsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  #share address
        if os.name != 'nt':
            # needed on Linux and OSX to share port with net core. Remove on windows
            self.rsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        try:
            self.rsock.bind(self.device_address)
        except:
            logger.error('Discovery responder: failure to bind receive socket')
            self.rsock.close()
            self.rsock = 0
            raise

        self.tsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.tsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  #share address
        try:
             self.tsock.bind((ADDR, 0))
        except:
            logger.error('Discovery responder: failure to bind send socket')
            self.tsock.close()
            self.tsock = 0
            raise
           
        # OK start the listener
        self.daemon = True
        self.start()
    def run(self):
        while True:
            data, addr = self.rsock.recvfrom(1024)
            datascii = str(data, 'ascii')
            logger.info(f'Disc rcv {datascii} from {str(addr)}')
            if 'alpacadiscovery1' in datascii:
                self.tsock.sendto(self.alpaca_response.encode(), addr)
