.. only:: html

    .. image:: alpaca128.png
        :height: 92px
        :width: 128px
        :align: right

Template/Sample Module Structure
=================================

The template/sample is organized into modules that implement the Alpaca API,
those which implement the actual physical device (a simulated Rotator here),
and support/boilerplate.

Alpaca API Implementation Modules
---------------------------------
These are the modules that contain the Falcon responder classes for each
of the Alpaca API endpoints, and the Alpaca exception specs.

.. toctree::
   :maxdepth: 1

   common
   rotator
   exceptions
   discovery

Physical Device Implementation
------------------------------

.. toctree::
   :maxdepth: 1

   rotatordevice

App and Support Logic
---------------------

.. toctree::
   :maxdepth: 1

   app
   config
   log
   shr

