
Exceptions - Classes Defining Alpaca Exceptions
===============================================

This module contains the ASCOM Exception classes. They are used to represent the
Alpaca-standard error codes and default error messages as input to construction
of all JSON responses. The error messages may be overridden (and probably should
be so as to give the most help to the app user).

.. note::
    When creating an instance, the exception is automatically logged,
    including any overridden error message.

Exception Classes
-----------------

.. automodule:: exceptions
    :members:
