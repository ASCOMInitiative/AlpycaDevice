
   .. image:: alpaca128.png
      :height: 92px
      :width: 128px
      :align: right

Migrating from Earlier Versions to Platform 7
=============================================

Your existing device will continue to run with no changes. However, we recommend that you
migrate to the Platform 7 version of your device's interface. For example, if you implemented
iTelescopeV3 with the 0.x version of this SDK, it will continue to work, but your telescope
mount will not support the |plat7relnotes|, which are in |itelescopev4|.

.. important::

    Your primary source of reference information is the |masterdoc| which covers
    Platform 7. Please review |plat7relnotes| first, so you understand the
    reasons for the additions to the interfaces, which are mostly to assure
    asynchronous operations for Alpaca.

Migration Summary
-----------------

1. Add one or more new :ref:`responder classes <responder-classes>` for the new properties and/or
   methods (members) to your existing responder module.
2. Increase the value of the ``Interface Version`` property to indicate to
   clients that your device supports the new interface members.
3. Use |conformu| to test your device for both Interface and Alpaca Protocol.

Adding New members
------------------

This is best done by doing a diff of your existing responder module, for
example, ``telescope.py`` with the ``telescope.py`` template that came with this
new version of the SDK. This will show you the new responder classes that cover
the new interface members. Copy from the template to your existing responder
module, then wire up the new responder(s) to your controller logic as before.

Updating ``InterfaceVersion``
-----------------------------

Clients will not know that your device adheres to the new interface until you
change the ``InterfaceVersion`` property reported by your device. For example,
upgrading from ``iTelescopeV3`` to ``iTelescopeV4`` you must change the value
returned by your ``Telescope.InterfaceVersion`` from 3 to 4.

Testing with |conformu|
-----------------------

Once you have implemented the new interface members and updated
``InterfaceVersion``, it's vital to test your device with |conformu|. The tool
honors ``InterfaceVersion`` so it will recognize that your device is now
compatible with the new interface for Platform 7, and itelescopev4 will test
these new members along with the others. Perform both the main Conformation test
as well as the Alpaca Protocol test. You will likely find places where you need
to make adjustments.

If you run into difficulties, please feel free to post to the |devgrp|

.. |plat7relnotes| raw:: html

    <a href="https://ascom-standards.org/newdocs/relnotes.html" target="_blank">
    new interface features of Platform 7</a>

.. |itelescopev4| raw:: html

    <a href="https://ascom-standards.org/newdocs/telescope.html" target="_blank">
    iTelescopeV4</a>

.. |conformu| raw:: html

    <a href="https://github.com/ASCOMInitiative/ConformU/releases" target="_blank">
    Conform Universal</a>

.. |masterdoc| raw:: html

    <a href="https://ascom-standards.org/newdocs/" target="_blank">
    ASCOM Master Interfaces</a>

.. |devgrp| raw:: html

    <a href="https://ascomtalk.groups.io/g/Developer" target="_blank">
    ASCOM Driver and Application Development Support Forum</a>

