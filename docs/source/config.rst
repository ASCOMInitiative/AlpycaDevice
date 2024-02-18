
Device Configuration Support
============================

To keep things simple, this template uses a text file in |toml| format
``./config.toml``. The :py:class:`~config.Config` class provides read-only access
to the various config options for this device that are in ``./config.toml``.

Of course you can alter these config items, making changes to the items
in ``./config.toml`` to accommodate your config needs.

Device-Specific Settings
------------------------

In the sample `config.toml`, the ``[device]`` section contain settings for
the Rotator sample. This is where you can put your device's settings. The
items that are there need to be reflected in the :py:class:`~config.Config`
class to provide named access to your driver's code.

Alternate Location of ``config.toml``
-------------------------------------

The :py:class:`~config.Config` class provides support for the config.toml
file to be located at ``/alpyca/config.toml`` (note the rooted path). This
makes it possible to store sensitive information for a specific driver
installation within (e.g.) a Docker container and avoid keeping sensitive
information in the driver repository. Any setting will first be retried from
``/alpyca/config.toml`` and if not found there, it will look in
``./config.toml``.

Config class
------------

.. module:: config

.. autoclass:: Config
    :members:
    :undoc-members:


.. |toml| raw:: html

     <a href="https://toml.io/en/" target="_blank">
    Tom's Obvious Minimal Language</a>
