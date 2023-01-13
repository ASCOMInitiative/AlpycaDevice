..
    The rinohtype PDF builder I use chokes on right-justified images
    failing to wrap them with the text. It also chokes on the |xxx|
    format hyperlinks to externals that I use for opening in a separate
    tab. Therefore I have html and rinoh conditionals in these docs (typ)

.. only:: html

    .. image:: alpaca128.png
        :height: 92px
        :width: 128px
        :align: right

Developer Roadmap
=================

.. caution::

    Before starting your development project, it is highly recommended that you
    take a few minutes to read through |princ|.

.. note::

    It's suggested that you make an Alpaca driver for a single ASCOM device type
    and a single instance of that device. This roadmap is written with that in mind.

Making this sample into your driver
-----------------------------------

When using this sample to make your own Alpaca device driver, follow this general
set of steps.

1. Familiarize yourself with |falcweb| specifically how incoming REST requests are
   routed to *responders* with the Request and Response objects.
2. Run this sample, using the |conformu| tool to generate traffic to all of the Rotator
   endpoints. Walk through the app startup in the :doc:`app` with the debugger.
   See how the API endpoint URIs are registered to the responder classes in the
   :py:func:`app.init_routes` function. Walk through
   a GET request, then a PUT request. See how the Alpaca JSON
   responses are created by the
   :py:class:`shr.PropertyResponse` and :py:class:`shr.MethodResponse` classes.
   Look how the simulated rotator machine
   is started and runs in a separate class. Observe how locks are used to prevent
   conflicts in accesses between threads. In short, become very familiar with how
   this simulated device works.
3. Using :doc:`/rotator` as a guide, and the responder classes within as a template,
   create a module containing responder classes for each Alpaca endpoint of *your* device.
   Of course, if you're making a Rotator driver you can use :doc:`/rotator` as a starting
   point.
4. Look in :doc:`shr` for the :py:class:`shr.DeviceMetadata` static class.
   Edit the fields for your device. Generate your own unique **ID** using the |guidgen|
5. Adjust the user configuration file (config.toml) for the Title, IP/Port etc.
6. Develop the low-level code to control your device. Try to design it so that it
   provides variables and functions that can be used by the Alpaca methods and
   properties. Obviously this is going to be the major portion of your work,
   followed by the time required to create the module containing the Alpaca endpoint
   responder classes (step 2 above).
7. Wire up the device control code to the endpoint responder classes.
8. Test and fix until your device passes the full Conform Universal test.
9. Use the Alpaca Protocol Tester in ConformU to check your driver at the Alpaca
   protocol level (as opposed to the operational tests provided by the
   Conformance checker.)

Alpaca Driver Request Flow - Responder Classes
----------------------------------------------

Incoming HTTP/REST requests from the client are routed through the server by Falcon,
and result in calls to the *responder* classes for the device API. For example, an app
would send the following HTTP request to see if the rotator is moving:

``/api/v1/rotator/0/ismoving?ClientID=xxx&ClientTransactionID=yyy``

Here is the code to handle a simple request for the Rotator's
:py:class:`~rotator.IsMoving` property. For simplicity we don't look at the
``CLientID``or the ``ClientTransactionID``.

    .. image:: ismoving.png
        :height: 264px
        :width: 700px
        :align: center

Preprocessor
~~~~~~~~~~~~

This is a decorator :py:class:`~shr.PreProcessRequest()` which is applied to all responder
classes. Its job is to quality check the request. It rejects illegal values for Alpaca ``ClientID``
and ``ClientTransactionID``. It also checks that the ``DeviceNumber`` is valid. If any of these
tests fail, it raises an HTTP ``400 Bad Request`` with a body containing a specific error message.

.. note::
    Raising an ``HTTPBadRequest`` [#f1]_ here immediately abandons processing and
    and sends an HTTP error. It cannot be an Alpaca response (which would have a ``200 OK``
    status) because the request is not even a legal Alpaca request.

GET responder
~~~~~~~~~~~~~

Once the request is deemed Alpaca-legal by the pre-processor, the responder's ``on_get()``
method is called if the API request is for a ``GET`` (get the value of a property).
The first thing you see is a call into the rotator
device to see if it is connected. If not, it's an Alpaca
:py:class:`~exceptions.NotConnectedException`. Then it tries to read the position from the
rotator device. If an exception is raised from within the device code, it's caught with
a generic ``except`` and results in an Alpaca :py:class:`~exceptions.DriverException`.
Otherwise, it uses a :py:class:`~shr.PropertyResponse` object to
construct the JSON for an Alpaca property response, including the retrieved position
value. For example:

.. code-block:: json
    :emphasize-lines: 2
    :caption: Alpaca property response

    {
        "Value": true               // It's moving
        "ClientTransactionID": 321,
        "ServerTransactionID": 1,   // Automatically bumped by PropertyResponse
        "ErrorNumber": 0,           // Success
        "ErrorMessage": "",
    }

It sets the ``Response.text`` to the above Alpaca JSON, and returns to Falcon, which
returns the JSON as the HTTP body with a ``200 OK`` status. That's it!

Alpaca Exceptions
~~~~~~~~~~~~~~~~~

Continuing with the above sample, note how the Alpaca
:py:class:`~exceptions.NotConnectedException` is returned to the remote app. The
:py:class:`~shr.PropertyResponse` constructor gets the Falcon ``Request`` object as
its first parameter. The second parameter, the Alpaca exception class
:py:class:`~exceptions.NotConnectedException` is used by
:py:class:`~shr.PropertyResponse` to get the Alpaca error number and an error message
with which it constructs the Alpaca JSON Response:

.. code-block:: json
    :emphasize-lines: 2,3
    :caption: Alpaca **NotConnectedException** response

    {
        "ErrorNumber": 1031,        // 0x407
        "ErrorMessage": "The device is not connected.",
        "Value": ""                 // App ignores this value if present
    }

It sets the ``Response.text`` to the above Alpaca JSON, and returns to Falcon, which
returns the JSON as the HTTP body with a ``200 OK`` status. Note that any Alpaca request
which gets to the responder always returns with an HTTP ``200 OK`` status, even though
the response might be an Alpaca exception like this.

.. tip::

    You can supply your own error message as an optional parameter to any of the
    Alpaca exception classes.

Alpaca DriverException - "Do it Right or Raise an Error"
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In the example above notice that the call into the device ``rot_dev.ismoving`` is guarded
by a ``try/except``. The Alpaca :py:class:`~exceptions.DriverException` is specified
for use by the device for any error or failure not covered by the Alpaca exceptions.

.. caution::
    It's vital that *any* problem encountered by your device be telegraphed back to
    the app via one of the Alpaca exceptions. For most problems, this will be the
    ``DriverException``.

The :py:class:`~exceptions.DriverException` has unique enhancements. Look now.
In the example above, note the construction of ``DriverException`` includes an
error code, a n automaticelly constructed
responder class name, and the Python exception object. This allows
``DriverException`` to construct a detailed error message that includes the API
endpoint name (the name of the responder class) and optionally includes
a Python traceback
(the :py:attr:`~config.Config.verbose_driver_exceptions` config option). Also, since
``DriverException`` can use error codes from 0x500 through 0xFFF, you can
supply an error code. These codes are for you to use and have no specified
meaning within Alpaca.

.. note::
    This may surprise you, but if your device runs into trouble after
    successfully starting an operation, you *must* raise an exception when
    the client app asks for the status of that operation. So if your Rotator
    accepted a request to move to a new angle, and then got jammed up or
    otherwise failed to successfully complete the move to the new angle,
    then ``Rotator.IsMoving`` must
    raise a ``DriverException`` with a detailed error message like "Rotator
    has failed, possible jam or cable wrap". In this case, even deep within
    your device code raise a Python ``RuntimeError`` exception with your
    detailed message. The boiler plate will turn this into a useful Alpaca
    ``DriverException``. The app should always check ``Rotator.IsMoving``
    to make sure that the move request completed successfully. See |async|.


Asynchronous Operations
-----------------------

All time-consuming device operations, such as slewing a mount, are implemented
in Alpaca as **asynchronous operations**. While you may be familiar with async programming
with an async/await type feature, the Alpaca model is one of explicit
endpoints acting as *initiators* and *completion
properties*. Clients may choose to wrap these actions in async constructions for their
languages, but we're on the other end. Please take a few minutes to read |async|.

Handling Exceptions
-------------------

It's vital that your driver implement the *prime directive* for distributed systems:

.. epigraph::
    *Do it right or raise an Exception*
    -- ASCOM Initiative

For a detailed description of this vital principle as it applies to ASCOM and Alpaca,
read through |excep|. It will only take a few minutes. We've tried to make this as
TL:DR-proof as we could.

Alpaca Exceptions
~~~~~~~~~~~~~~~~~

The JSON
responses to all Alpaca requests include ``ErrorNumber`` and ``ErrorMessage`` members. If
``ErrorNumber`` is 0 then the client considers the request to have been a success
(the ``ErrorMessage`` is ignored). Otherwise, a non-zero ``ErrorNumber`` in the JSON
response tells the client that an Alpaca exception was raised (see :doc:`exceptions`).
|apiref| (Sec. 2.8) describes these Alpaca exceptions. Each one has a specific error number.
The accompanying error message defaults to a generic descriptive message but you can override
the message with something more detailed and helpful (recommended) when you instantiate
the Apaca Exception class.

Python Exceptions
~~~~~~~~~~~~~~~~~

Within your driver, your code may raise Python Exceptions. So how do you
communicate a Python exception through your Alpaca API responder and back to the client?
The |apiref| specifies that the Alpaca :py:class:`~exceptions.DriverException` should be
used for all problems within the device and driver code. In this sample, the
:py:class:`~exceptions.DriverException` class is unique in that it accepts a Python

.. rubric:: Footnotes

.. [#f1] Exception defined by Falcon

..
    Below are links that will open in a separate browser tab for convenience.

.. |guidgen| raw:: html

    <a href="https://guidgenerator.com/online-guid-generator.aspx" target="_blank">
    Online GUID / UUID Generator</a> (external)

.. |conformu| raw:: html

    <a href="https://github.com/ASCOMInitiative/ConformU#readme" target="_blank">
    Conform Universal</a> (external)

.. |princ| raw:: html

    <a href="https://ascom-standards.org/AlpacaDeveloper/Principles.htm" target="_blank">
    The General Principles</a> (external)

.. |async| raw:: html

    <a href="https://ascom-standards.org/AlpacaDeveloper/Async.htm" target="_blank">
    Asynchronous APIs</a> (external)

.. |excep| raw:: html

    <a href="https://ascom-standards.org/AlpacaDeveloper/Exceptions.htm" target="_blank">
    Exceptions in ASCOM</a> (external)

.. |falcweb| raw:: html

    <a href="https://falcon.readthedocs.io/en/stable/" target="_blank">
    The Falcon Web Framework</a> (external)

.. |apiref| raw:: html

    <a href="https://github.com/ASCOMInitiative/ASCOMRemote/raw/master/Documentation/ASCOM%20Alpaca%20API%20Reference.pdf"
    target="_blank">Alpaca API Reference (PDF)</a> (external)



