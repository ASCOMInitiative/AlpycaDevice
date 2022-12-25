# 24-Dec-2022   rbd 0.1 Logging
import toml
import logging

global logger
logger = None   # Set to global logger at app startup
def set_conf_logger(lgr):
    logger = lgr
    
# Of course you can read this from a config file here
_s = '''
title = "Alpaca Sample Driver (Rotator)"

[network]
ip_address = '192.168.0.42'
mc_address = '192.168.0.255'
port = 5555

[server]
log_level = 'INFO'
log_to_stdout = false
location = 'Alvord Desert'
verbose_driver_exceptions = true

[device]
can_reverse = true
step_size = 1.0
steps_per_sec = 6
'''
_dict = toml.loads(_s)

class Config:

    # ---------------
    # Network Section
    # ---------------
    ip_address: str = _dict['network']['ip_address']
    mc_address: str = _dict['network']['mc_address']
    port: int = _dict['network']['port']
    # --------------
    # Server Section
    # --------------
    log_level: int = logging.getLevelName(_dict['server']['log_level'])  # Not documented but works (!!!!)
    log_to_stdout: str = _dict['server']['log_to_stdout']
    location: str = _dict['server']['location']
    verbose_driver_exceptions: bool = _dict['server']['verbose_driver_exceptions']
    # --------------
    # Device Section
    # --------------
    can_reverse: bool = _dict['device']['can_reverse']
    step_size: float = _dict['device']['step_size']
    steps_per_sec: int = _dict['device']['steps_per_sec']

