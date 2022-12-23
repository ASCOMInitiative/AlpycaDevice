import toml

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

