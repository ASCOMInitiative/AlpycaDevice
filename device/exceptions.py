# =======================================
# EXCEPTIONS.PY - Alpaca Exception Casses
# =======================================
#
# 17-Dec-2022   rbd 0.1 Initial edit for Alpaca sample/template
# 18-Dec-2022   rbd 0.1 Refactor to support optional overriding
#                       error message, and support DriverException
#                       with variable error number.
#
import traceback
exc_verbose = True      # True for verbose DriverException messages

class Success:
    def __init__(self):
        self.number: int = 0
        self.message: str = ''

    @property
    def Number(self) -> int:
        return self.number

    @property
    def Message(self) -> int:
        return self.message

class ActionNotImplementedException:
    def __init__(
            self, 
            message: str = 'The requested action is not implemented in this driver.'
        ):
        self.number = 0x40C
        self.message = message

    @property
    def Number(self) -> int:
        return self.number

    @property
    def Message(self) -> int:
        return self.message


# The device chooses a number between 0x500 and 0xFFF, and
# provides a helpful/specific error message. Asserts the
# error number within range.
#
# args:

class DriverException:
    """
    **Exception Class for Driver Internal Errors**
        This exception is used for device errors and other internal exceptions. 
        It can be instantiated with a captured exception object, and if so format 
        the Alpaca error message to include line number/module or optionally a 
        complete traceback of the exception. 
    """
    def __init__(
            self, 
            number: int = 0x500,
            message: str = 'Internal driver error - this should be more specific.',
            exc = None,  # Python exception info 
            full: bool = exc_verbose
        ):
        """Initialize the DeviceException object
        
        Args:
            number (int):   Alpaca error number between 0x500 and 0xFFF, your choice
            message (str):  Specific error message or generic if left blank (see above)
            exc:            Contents 'ex' of 'except Exception as ex:' If not included
                            then only message is included. If supplied, then a detailed
                            error message with traceback is created (see full parameter)
            full (bool):    If True, a full traceback is included in the message.
                            Defaulted True above with exc_verbose, may be overriden
                            at construction time.
        """
        assert number >= 0x500 and number <= 0xFFF, 'Programmer error, bad DriverException number'
        self.number = number
        if not exc is None:
            if full:
                self.fullmsg = f'{message}:\n{traceback.format_exc()}'  # TODO Safe if not explicitly using exc?
            else:
                self.fullmsg = f'{message}:\n{type(exc).__name__}: {str(exc)}'
        else:
            self.fullmsg = message

    @property
    def Number(self) -> int:
        return self.number

    @property
    def Message(self) -> int:
        return self.fullmsg


class InvalidOperationException:
    def __init__(
            self, 
            message: str = 'The requested operation cannot be undertaken at this time.'
        ):
        self.number = 0x40B
        self.message = message

    @property
    def Number(self) -> int:
        return self.number

    @property
    def Message(self) -> int:
        return self.message


class InvalidValueException:
    def __init__(
            self, 
            message: str = 'Invalid value given.'
        ):
        self.number = 0x401
        self.message = message

    @property
    def Number(self) -> int:
        return self.number

    @property
    def Message(self) -> int:
        return self.message


class NotConnectedException:
    def __init__(
            self, 
            message: str = 'The device is not connected.'
        ):
        self.number = 0x407
        self.message = message

    @property
    def Number(self) -> int:
        return self.number

    @property
    def Message(self) -> int:
        return self.message

class NotImplementedException:
    def __init__(
            self, 
            message: str = 'Property or method not implemented.'
        ):
        self.number = 0x400
        self.message = message

    @property
    def Number(self) -> int:
        return self.number

    @property
    def Message(self) -> int:
        return self.message

class ParkedException:
    def __init__(
            self, 
            message: str = 'Illegal operation while parked.'
        ):
        self.number = 0x408
        self.message = message

    @property
    def Number(self) -> int:
        return self.number

    @property
    def Message(self) -> int:
        return self.message

class SlavedException:
    def __init__(
            self, 
            message: str = 'Illegal operation while slaved.'
        ):
        self.number = 0x409
        self.message = message

    @property
    def Number(self) -> int:
        return self.number

    @property
    def Message(self) -> int:
        return self.message


class ValueNotSetException:
    def __init__(
            self, 
            message: str = 'The value has not yet been set.'
        ):
        self.number = 0x402
        self.message = message

    @property
    def Number(self) -> int:
        return self.number

    @property
    def Message(self) -> int:
        return self.message

