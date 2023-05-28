
Rotator - Device-Specific Responders
====================================

This module contains the Rotator device-specific responder classes for the Alpaca
REST endpoints which represent ASCOM interface members.
You would need to create a module like this for the device you
wish to handle in your driver (e.g., ``Focuser``). The interface to each of
these responder classes is identical, as
described in |falcweb| but with the Alpaca Device Number as an additional
parameter to the ``on_get()`` and ``on_put()`` methods.

The ASCOM standard interface members (properties and methods) are implemented
as separate responder classes here. Incoming Alpaca requests are mapped to
the responders. Thus, your device's low-level control code would be called
from within the ``on_get()`` and/or ``on_put()`` responder functions. Here
are the bare interfaces (*error handling omitted for clarity*).
See the :doc:`/roadmap` for details on how the responders work in this
template/sample.

.. note::

    * The ``devno`` parameter carries the Alpaca device number. This is used
      only if your Alpaca device supports more than one ASCOM device (e.g.
      two or more Rotators).
    * The ``PropertyResponse`` and ``MethodResponse`` classes take a second attribute
      for returning an Alpaca exception. If omitted, it defaults to Success
      (no exception).

**The maxdev = 1 Constant**

This constant is passed as a parameter to all ``PreProcessRequest()`` decorators.
It is used to range check the device number in requests. It should be 1 unless
your Alpaca device supports more than one ASCOM device of this type (e.g. two
or more rotators).

**Property (GET) Endpoint Responder**

This returns a **Value** in the JSON response (``response.text``):

.. code-block:: python
    :emphasize-lines: 4
    :caption: Sample GET responder (for a property)

    @before(PreProcessRequest(maxdev))
    class IsMoving:
        def on_get(self, req: Request, resp: Response, devnum: int):
            value = #whatever your device says
            resp.text = PropertyResponse(value, req).json

**Method (PUT) Endpoint Responder**

Initiates an action. Normally returns no value. Parameters for the method
are carried in the ``PUT`` request body, and are encoded as HTTP "form fields".
These are retrieved as a Python dictionary via the Falcon ``req.get_media()``
function.

.. code-block:: python
    :emphasize-lines: 5
    :caption: Sample PUT responder (for a method)

    @before(PreProcessRequest(maxdev))
    class MoveAbsolute:
        def on_put(self, req: Request, resp: Response, devnum: int):
            formdata = req.get_media()
            newpos = float(formdata['Position'])    # Position parameter
            # Whatever it takes to START the action
            resp.text = MethodResponse(req).json

API Responder Documentation
---------------------------

Each class is a responder for that specific member (property or method) of
the ASCOM IRotator specification.

.. note::
    Calls to ``on_get()`` and ``on_put()`` have the same arguments as described
    above and in |falcweb| plus the Alpaca DeviceNumber as the last
    argument.

.. attention::

    The ``CommandXxx()`` methods are deprecated. These are left over from
    the distant past. If you want to implement unique non-standard
    commands for your device, use the ``Action()`` and ``SupportedActions``
    members. In this sample all of these are marked as not implemented.

.. automodule:: rotator
    :members:


.. |falcweb| raw:: html

    <a href="https://falcon.readthedocs.io/en/stable/" target="_blank">
    The Falcon Web Framework</a>

