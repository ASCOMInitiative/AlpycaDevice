
Exceptions - Classes Defining Alpaca Exceptions
===============================================

This module contains the ASCOM Exception classes. They are used to represent the
Alpaca-standard error codes and default error messages as input to construction
of all JSON responses. The error messages may be overridden (and probably should
be so as to give the most help to the app user).

:py:class:`~exceptions.DriverException` is special. It takes an additional
parameter, a Python ``Exception`` object, and will produce a Alpaca ``ErrorMessge``
containing the Python runtime error info.

.. note::
    When creating an instance, the exception is automatically logged,
    including any overridden error message.

Exception Classes
-----------------

.. automodule:: exceptions
    :members:
