
   .. image:: alpaca128.png
      :height: 92px
      :width: 128px
      :align: right

Template/Sample Module Structure
=================================

The template/sample is organized into modules that implement the Alpaca API,
those which implement the actual physical device (a simulated Rotator here),
and support/boilerplate. Though you'll see usage info for the boilerplate,
you don't have to do anything beyond the things listed in :doc:`/quickstart`.

Alpaca API Implementation Modules
---------------------------------
The provided working rotator sample, and the device implementation templates
for all ASCOM device types.

.. toctree::
   :maxdepth: 1

   rotator
   templates

Physical Device Implementation
------------------------------

.. toctree::
   :maxdepth: 1

   rotatordevice

App Startup and Device Declarations
-----------------------------------

.. Important::
   For each device type module (template + enhancements) you include in the app, you must make
   a 1-line edit here so the app can support that app type. See the App Startup dsocumentation
   linked below.

.. toctree::
   :maxdepth: 1

   app

Boilerplate Support Logic
-------------------------

.. Caution::

   **STOP AND READ THIS** The support logic is virtually complete, connected and ready to go. The info here
   is strictly for your amazement and amusement

.. toctree::
   :maxdepth: 1

   exceptions
   discovery
   config
   log
   shr
