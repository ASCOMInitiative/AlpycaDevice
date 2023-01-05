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

    It's suggested that you make an Alpaca driver for a single device type and a single
    instance of that device. This roadmap is written with that in mind.

Making this sample into your driver
-----------------------------------

When using this sample to make your own Alpaca device driver, follow this general
set of steps.

1. Run this sample, using the |conformu| tool to generate traffic to all of the Rotator
   endpoints. Walk through the app startup in the :doc:`app` with the debugger.
   See how the endpoint classes are registered to the responder classes. Walk through
   a GET request, then a PUT request. See how the responses are created by the
   PropertyResponse and MethodResponse classes. Look how the simulated rotator machine
   is started and runs in a separate class. Observe how locks are used to prevent
   conflicts in accesses between threads. In short, become very familiar with how
   this simulated device works.
2. Using :doc:`/rotator` as a guide, and the responder classes within as a template,
   create a module containing responder classes for each Alpaca endpoint of your device.
   Of course, if you're making a Rotator driver you can use :doc:`/rotator` as a starting
   point.
3. Look in :doc:`shr` for the `DeviceMetadata` static class.
   Edit the fields for your device. Generate your own unique **ID** using the |guidgen|
4. Adjust the user configuration file (config.toml) for the Title, IP/Port etc.
5. Develop the low-level code to control your device. Try to design it so that it
   provides variables and functions that can be used by the Alpaca methods and
   properties. Obviously this is going to be the major portion of your work,
   followed by the time required to create the module containing the Alpaca endpoint
   responder classes (step 2 above).
6. Wire up the device control code to the endpoint responder classes.
7. Test and fix until your device passes the full Conform Universal test.
8. Use the Alpaca Protocol Tester in ConformU to check your driver at the Alpaca
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



