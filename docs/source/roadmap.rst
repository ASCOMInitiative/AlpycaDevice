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
   a GET request, then a PUT request. See how the responses are created by the
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
|apiref| describes these Alpaca exceptions. Each one has a specific error number. The
accompanying error message defaults to a generic descriptive message but you can override
the message with something more detailed and helpful (recommended) when you instantiate
the Apaca Exception class.

Python Exceptions
~~~~~~~~~~~~~~~~~

Within your driver, your code may raise Python Exceptions. So how do you
communicate a Python exception through your Alpaca API responder and back to the client?
The |apiref| specifies that the Alpaca :py:class`exceptions.DriverException` should be
used for all problems within the device and driver code. In this sample, the
:py:class`exceptions.DriverException` class is unique in that it accepts a Python


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



