
Common - Responders common to all Alpaca Devices
================================================

This module contains the responder classes for the Alpaca
REST endpoints which represent ASCOM interface members that are common
to all ASCOM devices. You should not need to edit this at all if
you don't use ``CommandXxx()``, ``Action()``, or ``SupportedActions``, since the
metadata is taken from the ``config.toml`` device config file.

.. attention::

    The ``CommandXxx()`` methods are deprecated. These are left over from
    the distant past. If you want to implement unique non-standard
    commands for your device, use the ``Action()`` and ``SupportedActions``
    members. In this sample all of these are marked as not implemented.

The interface to each of
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

**Property (GET) Endpoint Responder**

This returns a **Value** in the JSON response (``response.text``):

.. code-block:: python
    :emphasize-lines: 4
    :caption: Sample GET responder (for ``Description`` property)

    @before(PreProcessRequest())
    class Description():
        def on_get(self, req: Request, resp: Response, devnum: int):
            resp.text = PropertyResponse(DeviceMetadata.Description, req).json


API Responder Documentation
---------------------------

.. automodule:: common
    :members:
    :undoc-members:


.. |falcweb| raw:: html

    <a href="https://falcon.readthedocs.io/en/stable/" target="_blank">
    The Falcon Web Framework</a>

