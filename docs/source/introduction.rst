.. image:: alpaca128.png
    :height: 92px
    :width: 128px
    :align: right

==============================
Introduction to Alpaca Drivers
==============================

Writing a successful device driver requires, first and foremost, a clear
understanding of the role of a driver, and by extension, the responsibilities of
the driver and the developer. There are subtleties and easily missed aspects. We
can't overstress the importance of starting a driver project with a clear view
of the landscape. These documents will give you a good overview of driver
development.

1. |ascsite| All things ASCOM and Alpaca
2. |devhelp| See the Design Principles sections: General Principles,
   Asynchronous APIs, and  Exceptions.
3. |apiref| General specifications for Alpaca network protocol and API
4. |ascspecs|

Alpaca Device and Driver Architecture
-------------------------------------

An "Alpaca device" consists of a **server** which can host one or more
**drivers** for *multiple* ASCOM devices of *multiple* types. For example, a
single Alpaca device could provide the HTTP/REST communications for two ASCOM
cameras and an ASCOM mount, all through the same IP address and port.

The device's internal **server** is an HTTP (web) server that apps talk to using
the Alpaca HTTP/REST protocol, and which dispatches endpoint requests as calls
to the drivers for each device type and instance.

An ASCOM **device driver** consists of a set of *responders* for each Alpaca
REST endpoint (represented by a unique URI), including the ones common to all
ASCOM devices like ``Description`` and ``DriverVersion``, as well as the ones
specific to the ASCOM device type like ``Rotator.MoveMechanical()``. Incoming
REST requests are *routed* to their respective responders. The responder is
responsible for performing the action or accessing the data represented by the
endpoint.

.. important::
    Each member of the ASCOM interface for a device is mapped
    one-for-one to an Alpaca REST endpoint and thence to a responder
    for that endpoint. This one-for-one mapping makes interoperation
    between ASCOM Alpaca and classic ASCOM/COM possible.

Each endpoint URI contains both the device type (its device name) and also a
device number (the particular instance of that device type). The server is
responsible for calling the responder for the device type and instance.
Typically this is done via a routing table.

The Alpaca device's server is additionally responsible for responding to Alpaca
``Discovery`` multicasts coming from clients. This is a really simple mechanism.
It sends back a simple JSON response ``{AlpacaPort: *n*}``. Together with this
port number, and the server's IP address in the HTTP response packet, the client
now knows now to talk to the Alpaca server.

Once a client has found the Alpaca device, it can talk to its internal server to
determine the types of ASCOM devices served, and the number of instances of each
ASCOM device that are available (and some other metadata). This is done through
three ``Management`` endpoints. These are typically used by client apps to
select a specific device served [#]_

Finally, device settings and configuration are optionally provided with a set of
HTML web pages via the ``setup`` endpoint. Alternatively, for lightweight
applications (like this sample) an alternative is to use a simple text config
file.

.. hint::
    For details see |apiref|

Sample Driver Organization
--------------------------

In this sample the HTTP server function is provided by the lightweight Python
|wsgiref| combined with the |falcweb|. These two components together provide the
REST API engine and endpoint URI-to-responder routing. The HTTP server and the
Falcon back-end application are created on the main thread at app startup and
run "forever".

The responders for each Alpaca device API are kept in separate modules, one for
the endpoints common to all device types, and the other for the device-specific
endpoints. In this sample, these are ``common.py`` and ``rotator.py``.

.. note:: Your main development effort will focus on the device-specific
    responder classes. Metadata elsewhere can be tailored quickly.

Routing of incoming requests to the responder classes is done with a simple
function ``app.init_routes()`` which inspects each .py module containing
responder classes, finds each class, constructs the endpoint URI template and
then enters the URI and responder class into the Falcon routing table. Thus you
do not need to manually create routes for responders. See |falcweb|.

Alpaca discovery is provided by a simple engine running in a separate thread. It
is started at app startup, and runs "forever". You should not need to edit this.

Management API is provided in a separate module and routing for the management
endpoits is set up at app startup.

Logging is provided by the standard Python logger engine, with customizations
for the logging format including ISO-8601/UTC time stamps and logging to a file
(and optionally stdout). In addition, the HTTP server's logging output, normally
coming at the *end* of a request, is replaced with an HTTP request log at the
*beginning* of the request so that it is in context with logged messages that
may appear during processing of requests. The HTTP server is allowed to write
the post-request log line for non-200 (OK) HTTP responses.

Finally the ``setup`` endpoint simply displays a static web page. Configuration
for this lightweight sample uses a config file in |toml|. Of course you can
provide your own web pages, or get really fancy and use |falcjinja|.

.. _async-intro:

Asynchronous Operations
-----------------------

All time-consuming device operations, such as slewing a mount, are implemented
in Alpaca as **asynchronous operations**. While you may be familiar with async
programming with an async/await type feature, the Alpaca base model is one of
explicit endpoints acting as *initiators* and *completion properties*.

.. attention::

    * Your device and the responders in the driver must return promptly to every call.
    * This may surprise you, but if your device runs into trouble after
      successfully starting an operation, you *should* raise an exception when
      the client app later asks for the status of that operation. See |async|.
      test


.. _excep-intro:

Handling Exceptions
-------------------

It's vital that your driver implement the *prime directive* for distributed
systems:

.. epigraph::
    *Do it right or raise an Exception*
    -- ASCOM Initiative

For a detailed description of this vital principle as it applies to ASCOM and
Alpaca, read through |excep|. It will only take a few minutes. We've tried to
make this as TL:DR-proof as we could.

Alpaca Exceptions
~~~~~~~~~~~~~~~~~

The JSON responses to all Alpaca requests include ``ErrorNumber`` and
``ErrorMessage`` members. If ``ErrorNumber`` is 0 then the client considers the
request to have been a success (the ``ErrorMessage`` is ignored). Otherwise, a
non-zero ``ErrorNumber`` in the JSON response tells the client that an Alpaca
exception was raised (see :doc:`exceptions`). |apiref| (Sec. 2.8) describes
these Alpaca exceptions. Each one has a specific error number. The accompanying
error message defaults to a generic descriptive message but you can override the
message with something more detailed and helpful (recommended) when you
instantiate the Apaca Exception class.

Python Exceptions
~~~~~~~~~~~~~~~~~

Within your driver, your code may raise Python Exceptions. So how do you
communicate a Python exception through your Alpaca API responder and back to the
client? The |apiref| specifies that the Alpaca
:py:class:`~exceptions.DriverException` should be used for all problems within
the device and driver code. In this sample, the
:py:class:`~exceptions.DriverException` class is unique in that it accepts a
Python

.. tip::

    The built-in exception handling in this template/sample is detailed in the
    :doc:`/roadmap`.


Making this sample into your driver
-----------------------------------

When using this sample to make your own Alpaca device driver, follow this
general set of steps.

.. important::
    The |ascspecs| are the final word in interface definition, data types,
    exceptions, and behavior. Experiment with the |omnisim| OpenAPI interface
    to see how each endpoint is supposed to work.

1. Familiarize yourself with |falcweb| specifically how incoming REST requests
   are routed to *responders* with the Request and Response objects.
2. Run this sample, using the |conformu| tool to generate traffic to all of the
   Rotator endpoints. Walk through the app startup in the :doc:`app` with the
   debugger. See how the API endpoint URIs are registered to the responder
   classes in the :py:func:`~app.init_routes` function. Walk through a GET
   request, then a PUT request. See how the Alpaca JSON responses are created by
   the :py:class:`~shr.PropertyResponse` and :py:class:`~shr.MethodResponse`
   classes. Look how the simulated rotator machine is started and runs in a
   separate class. Observe how locks are used to prevent conflicts in accesses
   between threads. In short, become very familiar with how this simulated
   device works.
3. Using :doc:`/rotator` as a guide, and one of the :doc:`/templates` provided
   create a module containing responder classes for each Alpaca endpoint of
   *your* device.  Using the one for your device will be a big time saver!! Of
   course, if you're making a Rotator driver you can use :doc:`/rotator` as a
   starting point.
4. Look in :doc:`shr` for the :py:class:`~shr.DeviceMetadata` static class. Edit
   the fields for your device. Generate your own unique **ID** using the
   |guidgen|.
5. Adjust the user configuration file (config.toml) for the Title, IP/Port etc.
6. Develop the low-level code to control your device. Try to design it so that
   it provides variables and functions that can be used by the Alpaca methods
   and properties. Obviously this is going to be the major portion of your work,
   followed by the time required to create the module containing the Alpaca
   endpoint responder classes (step 2 above).
7. Wire up the device control code to the endpoint responder classes.
8. Test and fix until your device passes the full |conformu| tool's test.
9. Use the Alpaca Protocol Tester in ConformU to check your driver at the Alpaca
   protocol level (as opposed to the operational tests provided by the
   Conformance checker.)


.. |ascsite| raw:: html

    <a href="https://ascom-standards.org/index.htm" target="_blank">
    ASCOM Initiative web site</a>

.. |ascspecs| raw:: html

    <a href="https://ascom-standards.org/newdocs/" target="_blank">
    Master Generic ASCOM Device Interface Specifications</a>

.. |devhelp| raw:: html

    <a href="https://ascom-standards.org/AlpacaDeveloper/Index.htm" target="_blank">
    Alpaca Developers Info</a>

.. |async| raw:: html

    <a href="https://ascom-standards.org/AlpacaDeveloper/Async.htm" target="_blank">
    Asynchronous APIs</a>

.. |excep| raw:: html

    <a href="https://ascom-standards.org/AlpacaDeveloper/Exceptions.htm" target="_blank">
    Exceptions in ASCOM</a>

.. |guidgen| raw:: html

    <a href="https://guidgenerator.com/online-guid-generator.aspx" target="_blank">
    Online GUID / UUID Generator</a>

.. |conformu| raw:: html

    <a href="https://github.com/ASCOMInitiative/ConformU#readme" target="_blank">
    Conform Universal</a>

.. |apiref| raw:: html

    <a href="https://github.com/ASCOMInitiative/ASCOMRemote/raw/master/Documentation/ASCOM%20Alpaca%20API%20Reference.pdf"
    target="_blank">Alpaca API Reference (PDF)</a>

.. |supforum| raw:: html

    <a href="https://ascomtalk.groups.io/g/Developer" target="_blank">
    ASCOM Driver and Application Development Support Forum</a>


.. |omnisim| raw:: html

    <a href="https://github.com/ASCOMInitiative/ASCOM.Alpaca.Simulators#readme" target="_blank">
    Alpaca Omni Simulator</a>

.. |falcweb| raw:: html

    <a href="https://falcon.readthedocs.io/en/stable/" target="_blank">
    The Falcon Web Framework</a>

.. |wsgiref| raw:: html

    <a href="https://docs.python.org/3/library/wsgiref.html#module-wsgiref.simple_server" target="_blank">
    wsgiref.simple_server</a>

.. |toml| raw:: html

     <a href="https://toml.io/en/" target="_blank">
    Tom's Obvious Minimal Language</a>

.. |falcjinja| raw:: html

     <a href="https://github.com/myusko/falcon-jinja" target="_blank">
    Falcon support for Jinja-2</a>


.. [#] The Windows ASCOM Chooser uses discovery and the management
    endpoints to provide the user with the devices to select from.


