
Master Logger Support
=====================

This contains the logic that creates a custom Python logger which is used
throughout this Alpaca driver app. The Python construction details are within
the initialization function.

.. attention::

    For more details see :ref:`logging_support`.

The logger may be called from anywhere. Look at the ``rotatordevice.py``
module to see how it is constructed, including the app passing the Logger
reference as an initilization paremeter.

.. automodule:: log
    :members:
    :undoc-members:

