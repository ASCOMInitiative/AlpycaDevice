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

Introduction
============

.. note::
    Writing a successful device driver requires, first and foremost, a clear understanding
    of the role of a driver, and by extension, the responsibilities of the driver and
    the developer. There are subtleties and easily missed aspects. We can't overstress
    the importance of starting a driver project with a clear view of the landscape.

.. only:: html

    These documents will give you a good overview of driver development.

    1. |ascsite| All things ASCOM and Alpaca
    2. |devhelp| See the Design Principles sections: General Principles, Asynchronous APIs, and  Exceptions.
    3. |apiref| General specifications for Alpaca network protocol and API

.. only:: rinoh

    These documents will give you a good overview of driver development.

    1. `ASCOM Initiative web site <https://ascom-standards.org/index.htm>`_ All things ASCOM and Alpaca
    2. `Alpaca Developers Info <https://ascom-standards.org/AlpacaDeveloper/Index.htm>`_ See the Design Principles sections: General Principles, Asynchronous APIs, and  Exceptions.
    3. `Alpaca API Reference (PDF) <https://github.com/ASCOMInitiative/ASCOMRemote/raw/master/Documentation/ASCOM%20Alpaca%20API%20Reference.pdf>`_ General specifications for Alpaca network protocol and API

Alpaca Server and Driver Architecture
-------------------------------------

An Alpaca device consists of a **server** which can host one or more **drivers**
for *multiple* ASCOM devices of *multiple* types. For example, a single Alpaca device
could provide the HTTP/REST communications for two ASCOM cameras and an ASCOM
mount, all through the same IP address and port.

The device's internal **server** is an HTTP (web) server that apps talk to using the
Alpaca HTTP/REST protocol, and which dispatches endpoint requests as calls to the
drivers for each device type and instance.

An ASCOM **device driver** consists of a set of *responder* classes for each
Alpaca endpoint,
including the ones common to all ASCOM devices like ``Description`` and
``DriverVersion``,
as well as the ones specific to the ASCOM device type like
``Rotator.MoveMechanical()``.
Incoming REST requests are *routed* to their respective responder class.
The responder is responsible for performing the action or accessing the data
represented by the endpoint. Thus, each member of the ASCOM interface for a
device is mapped one-for-one to an Alpaca REST endpoint and thence to a responder
class for that endpoint.

The endpoint URI contains both the device type (its device name) and also a
device number (the particular instance of that device type). The server instance
responsible for calling the responder for the device type and instance. Typically
this is done via a routing table.

The Alpaca device's server is additionally responsible for
responding to Alpaca ``Discovery``
multicasts coming from clients. This is a really simple mechanism. It sends back
a simple JSON response ``{AlpacaPort: *n*}``. Together with this port number,
and the server's IP address in the HTTP response packet, the client now knows
now to talk to the Alpaca server.

Once a client has found the Alpaca device, it can talk to its internal server
to determine the types of ASCOM devices
served, and the number of instances of each ASCOM device that are
available (and some
other metadata). This is done through three ``Management`` endpoints. These
are typically used by client apps to select a specific device served [#]_

Finally, device settings and configuration are optionally provided with a set of
HTML web pages via the ``setup`` endpoint. Alternatively, for lightweight
applications (like this sample) an alternative is to use a simple text
config file.

.. hint::
    For details see |apiref|

Sample Driver Organization
--------------------------

In this sample the HTTP server function is provided by the
lightweight Python |wsgiref| combined with the |falcweb|. These two
components together provide the REST API engine for the actual driver).
the server and the Falcon back-end application are created on the
main thread at app startup and run "forever".

The responders for each Alpaca device API are kept in separate modules, one
for the endpoints common to all device types, and the other for the
device-specific endpoints. In this sample, these are ``common.py`` and
``rotator.py``.

.. note:: Your main development effort will focus on the device-specific
    responder classes. Metadata elsewhere can be tailored quickly.

Routing of incoming requests to the responder classes is done with a simple
function ``app.init_routes()`` which inspects each .py module containing
responder classes, finds each class, constructs the endpoint URI template
and then enters the URI and responder class into the Falcon routing table. Thus you
do not need to manually create routes for responders. See |falcweb|.

Alpaca discovery is provided by a simple engine running in a separate thread.
It is started at app startup, and runs "forever". You should not need to edit this.

Management API is provided in a separate module and routing for the management
endpoits is set up at app startup.

Logging is provided by the standard Python logger engine, with customizations
for the logging format including ISO-8601/UTC time stamps and logging to a file
(and optionally stdout). In addition, the HTTP server's logging output, normally
coming at the *end* of a request, is replaced with an HTTP request log at
the *beginning* of the request so that it is in context with logged messages
that may appear during processing of requests. The HTTP server is allowed to
write the post-request log line for non-200 (OK) HTTP responses.

Finally the ``setup`` endpoint simply displays a static web page. Configuration
for this lightweight sample uses a config file in |toml|. Of course you can
provide your own web pages, or get really fancy and use |falcjinja|.



.. |ascsite| raw:: html

    <a href="https://ascom-standards.org/index.htm" target="_blank">
    ASCOM Initiative web site</a> (external)

.. |devhelp| raw:: html

    <a href="https://ascom-standards.org/AlpacaDeveloper/Index.htm" target="_blank">
    Alpaca Developers Info</a> (external)

.. |apiref| raw:: html

    <a href="https://github.com/ASCOMInitiative/ASCOMRemote/raw/master/Documentation/ASCOM%20Alpaca%20API%20Reference.pdf"
    target="_blank">Alpaca API Reference (PDF)</a> (external)

.. |supforum| raw:: html

    <a href="https://ascomtalk.groups.io/g/Developer" target="_blank">
    ASCOM Driver and Application Development Support Forum</a> (external)


.. |omnisim| raw:: html

    <a href="https://github.com/ASCOMInitiative/ASCOM.Alpaca.Simulators#readme" target="_blank">
    Alpaca Omni Simulator</a> (external)

.. |falcweb| raw:: html

    <a href="https://falcon.readthedocs.io/en/stable/" target="_blank">
    The Falcon Web Framework</a> (external)

.. |wsgiref| raw:: html

    <a href="https://docs.python.org/3/library/wsgiref.html#module-wsgiref.simple_server" target="_blank">
    wsgiref.simple_server</a> (external)

.. |toml| raw:: html

     <a href="https://toml.io/en/" target="_blank">
    Tom's Obvious Minimal Language</a> (external)

.. |falcjinja| raw:: html

     <a href="https://github.com/myusko/falcon-jinja" target="_blank">
    Falcon support for Jinja-2</a> (external)


.. [#] The Windows ASCOM Chooser uses discovery and the management
    endpoints to provide the user with the devices to select from.


