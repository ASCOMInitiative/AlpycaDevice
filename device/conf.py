# 24-Dec-2022   rbd 0.1 Logging
# 25-Dec-2022   rbd 0.1 More config items, separate logging section
import toml
import logging
 
# Of course you can read this from a config file here
_s = '''
title = "Alpaca Sample Driver (Rotator)"

[network]
ip_address = '192.168.0.42'
mc_address = '192.168.0.255'
port = 5555

[server]
location = 'Alvord Desert'
verbose_driver_exceptions = true

[device]
can_reverse = true
step_size = 1.0
steps_per_sec = 6

[logging]
log_level = 'INFO'
log_to_stdout = false
max_size_mb = 5
num_keep_logs = 10
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
    location: str = _dict['server']['location']
    verbose_driver_exceptions: bool = _dict['server']['verbose_driver_exceptions']
    # --------------
    # Device Section
    # --------------
    can_reverse: bool = _dict['device']['can_reverse']
    step_size: float = _dict['device']['step_size']
    steps_per_sec: int = _dict['device']['steps_per_sec']
    # ---------------
    # Logging Section
    # ---------------
    log_level: int = logging.getLevelName(_dict['logging']['log_level'])  # Not documented but works (!!!!)
    log_to_stdout: str = _dict['logging']['log_to_stdout']
    max_size_mb: int = _dict['logging']['max_size_mb']
    num_keep_logs: int = _dict['logging']['num_keep_logs']


