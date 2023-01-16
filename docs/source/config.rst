
Device Configuration Support
============================

To keep things simple, this template uses a simple text file in |toml| format
``config.toml``.
The :py:class:`~config.Config` class provides read-only access to the
various config options for this device.

Of course you can alter these config items, making changes to the
:py:class:`~config.Config` class to accommodate your config needs.

.. module:: config

.. autoclass:: Config
    :members:
    :undoc-members:


.. |toml| raw:: html

     <a href="https://toml.io/en/" target="_blank">
    Tom's Obvious Minimal Language</a> (external)
