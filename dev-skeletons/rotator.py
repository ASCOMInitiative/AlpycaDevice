
# -*- coding: utf-8 -*-
#
# -----------------------------------------------------------------------------
# rotator.py - Alpaca API responders for rotator
#
# Author:   Your R. Name <your@email.org> (abc)
#
# -----------------------------------------------------------------------------
# Edit History:
#   Generated by Python Interface Generator for AlpycaDevice
#
# ??-???-????   abc Initial edit

from falcon import Request, Response, HTTPBadRequest, before
from logging import Logger
from shr import PropertyResponse, MethodResponse, PreProcessRequest, \
                get_request_field, to_bool
from exceptions import *        # Nothing but exception classes

logger: Logger = None

@before(PreProcessRequest())
class canreverse:

    def on_get(self, req: Request, resp: Response, devnum: int):
        try:
            # ----------------------
            val = ## GET PROPERTY ##
            # ----------------------
            resp.text = PropertyResponse(val, req).json
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                            DriverException(0x500, f'{self.__class__.__name__} failed', ex)).json

@before(PreProcessRequest())
class ismoving:

    def on_get(self, req: Request, resp: Response, devnum: int):
        try:
            # ----------------------
            val = ## GET PROPERTY ##
            # ----------------------
            resp.text = PropertyResponse(val, req).json
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                            DriverException(0x500, f'{self.__class__.__name__} failed', ex)).json

@before(PreProcessRequest())
class mechanicalposition:

    def on_get(self, req: Request, resp: Response, devnum: int):
        try:
            # ----------------------
            val = ## GET PROPERTY ##
            # ----------------------
            resp.text = PropertyResponse(val, req).json
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                            DriverException(0x500, f'{self.__class__.__name__} failed', ex)).json

@before(PreProcessRequest())
class position:

    def on_get(self, req: Request, resp: Response, devnum: int):
        try:
            # ----------------------
            val = ## GET PROPERTY ##
            # ----------------------
            resp.text = PropertyResponse(val, req).json
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                            DriverException(0x500, f'{self.__class__.__name__} failed', ex)).json

@before(PreProcessRequest())
class reverse:

    def on_get(self, req: Request, resp: Response, devnum: int):
        try:
            # ----------------------
            val = ## GET PROPERTY ##
            # ----------------------
            resp.text = PropertyResponse(val, req).json
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                            DriverException(0x500, f'{self.__class__.__name__} failed', ex)).json

    def on_put(self, req: Request, resp: Response, devnum: int):
        formdata = req.get_media()
        ##PARAMVAL## = ##PARAMCVT##formdata['##PARAMNAME##'])
        try:
            # -----------------------------
            ### DEVICE OPERATION(PARAM) ###
            # -----------------------------
            resp.text = MethodResponse(req).json
        except Exception as ex:
            resp.text = MethodResponse(req,
                            DriverException(0x500, f'{self.__class__.__name__} failed', ex)).json

@before(PreProcessRequest())
class stepsize:

    def on_get(self, req: Request, resp: Response, devnum: int):
        try:
            # ----------------------
            val = ## GET PROPERTY ##
            # ----------------------
            resp.text = PropertyResponse(val, req).json
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                            DriverException(0x500, f'{self.__class__.__name__} failed', ex)).json

@before(PreProcessRequest())
class targetposition:

    def on_get(self, req: Request, resp: Response, devnum: int):
        try:
            # ----------------------
            val = ## GET PROPERTY ##
            # ----------------------
            resp.text = PropertyResponse(val, req).json
        except Exception as ex:
            resp.text = PropertyResponse(None, req,
                            DriverException(0x500, f'{self.__class__.__name__} failed', ex)).json

@before(PreProcessRequest())
class halt:

    def on_put(self, req: Request, resp: Response, devnum: int):
        formdata = req.get_media()
        ##PARAMVAL## = ##PARAMCVT##formdata['##PARAMNAME##'])
        try:
            # -----------------------------
            ### DEVICE OPERATION(PARAM) ###
            # -----------------------------
            resp.text = MethodResponse(req).json
        except Exception as ex:
            resp.text = MethodResponse(req,
                            DriverException(0x500, f'{self.__class__.__name__} failed', ex)).json

@before(PreProcessRequest())
class move:

    def on_put(self, req: Request, resp: Response, devnum: int):
        formdata = req.get_media()
        ##PARAMVAL## = ##PARAMCVT##formdata['##PARAMNAME##'])
        try:
            # -----------------------------
            ### DEVICE OPERATION(PARAM) ###
            # -----------------------------
            resp.text = MethodResponse(req).json
        except Exception as ex:
            resp.text = MethodResponse(req,
                            DriverException(0x500, f'{self.__class__.__name__} failed', ex)).json

@before(PreProcessRequest())
class moveabsolute:

    def on_put(self, req: Request, resp: Response, devnum: int):
        formdata = req.get_media()
        ##PARAMVAL## = ##PARAMCVT##formdata['##PARAMNAME##'])
        try:
            # -----------------------------
            ### DEVICE OPERATION(PARAM) ###
            # -----------------------------
            resp.text = MethodResponse(req).json
        except Exception as ex:
            resp.text = MethodResponse(req,
                            DriverException(0x500, f'{self.__class__.__name__} failed', ex)).json

@before(PreProcessRequest())
class movemechanical:

    def on_put(self, req: Request, resp: Response, devnum: int):
        formdata = req.get_media()
        ##PARAMVAL## = ##PARAMCVT##formdata['##PARAMNAME##'])
        try:
            # -----------------------------
            ### DEVICE OPERATION(PARAM) ###
            # -----------------------------
            resp.text = MethodResponse(req).json
        except Exception as ex:
            resp.text = MethodResponse(req,
                            DriverException(0x500, f'{self.__class__.__name__} failed', ex)).json

@before(PreProcessRequest())
class sync:

    def on_put(self, req: Request, resp: Response, devnum: int):
        formdata = req.get_media()
        ##PARAMVAL## = ##PARAMCVT##formdata['##PARAMNAME##'])
        try:
            # -----------------------------
            ### DEVICE OPERATION(PARAM) ###
            # -----------------------------
            resp.text = MethodResponse(req).json
        except Exception as ex:
            resp.text = MethodResponse(req,
                            DriverException(0x500, f'{self.__class__.__name__} failed', ex)).json

