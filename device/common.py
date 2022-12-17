# ==============================================================
# COMMON.PY - Endpoints for members common to all Alpaca devices
# ==============================================================
#
# 16-Dec-2022   rbd 0.1 Initial edit for Alpaca sample/template
#
import falcon
from shr import *

# --------------------
# RESOURCE CONTROLLERS
# --------------------

class DriverVersion():
    def on_get(self, req: falcon.Request, resp: falcon.Response):
        resp.text = PropertyResponse(s_DriverVersion, req).json

