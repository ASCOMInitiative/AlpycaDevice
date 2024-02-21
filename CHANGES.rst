Version 0.7.0 Experimental (2024-02-20, for Platform 7)
=======================================================
* Add setting ``sync_write_connected`` to control whether writing
  ``True`` to ``Rotator.Connected`` acts synchrnonously
  or asynchronously. Conform assumes this deprecated action acts
  synchronously, so this defaults to ``True`` (see ``config.toml``)

Version 0.6.0 Experimental (2024-02-18, for Platform 7)
=======================================================
* Upgrade Rotator example to ``IRotatatorV4``, complete ConformU
  Validation and Alpaca Protocol Tests.
* Replace docstrings in Rotator example with links to the
  expanded interface member documentation in the
  `ASCOM Master Interfaces <https://ascom-standards.org/newdocs/>`_.
* Upgrade the device template generator to use JSON instead of YAML.
* Using Platform 7 JSON, generate new templates for all devices to
  include additional interface members for Platform 7.
* Update and enhance the
  `SDK documentation <https://ascom-standards.org/alpycadevice/>`_.
* References in documentation changed to reference the new
  `ASCOM Master Interfaces <https://ascom-standards.org/newdocs/>`_.
* Applied
  `GitHub Pull Request #11 <https://github.com/ASCOMInitiative/AlpycaDevice/pull/11>`_
  and added feature to documentation.
* Improved the formatting of the "Read the Docs" style for readability, and
  allowing flowed variable page size.

Version 0.5.0 Experimental (2023-11-28)
=======================================
* Fixed Connected class in several ways. See
  `GitHub Issue #10 <https://github.com/BobDenny/AlpycaDevice/issues/10>`_
* Regenerated all templates.

Version 0.4.0 Experimental (2023-11-08)
=======================================
* Fix templates to remove ``to_int()`` and ``to_float()`` from import
  of ``shr``, These were eliminated  in earlier refactoring.
  `GitHub Issue #6 <https://github.com/BobDenny/AlpycaDevice/issues/6>`_.
* Rename ``rotator.log`` in ``log.py`` module to ``alpyca.log`` since this server can
  support multiple device types. Update QuickStart to mention
  that the name may be changed to match the single device type (dome e.g.).
  `GitHub Issue #7 <https://github.com/BobDenny/AlpycaDevice/issues/7>`_.
* Add missing Connected member to all device type templates
  `GitHub Issue #8 <https://github.com/BobDenny/AlpycaDevice/issues/8>`_.
* Fixed the template generator app to avoid adding duplicate and
  fragmentary `on_put()` calls in addition to the correct ones.
  `GitHub Issue #9 <https://github.com/BobDenny/AlpycaDevice/issues/9>`_.
* Regenerated all templates.

Version 0.3.0 Experimental (2023-06-01)
=======================================
* Refactoring for multi-device types, mainly movement of the common endpoints
  into the individual device modules, so they can be implemented separately
  for each device *types*. Same with metadata. This covers
  `GitHub Issue #1 <https://github.com/BobDenny/AlpycaDevice/issues/1>`_
  and
  `GitHub Issue #3 <https://github.com/BobDenny/AlpycaDevice/issues/3>`_.
* Enhancment of templates to add explicit names and procesing of PUT parameters
  and for proper exception reporting. This includes
  `GitHub Issue #2 <https://github.com/BobDenny/AlpycaDevice/issues/2>`_.
* Passes the new Alpaca Protocol checker (this required numerous changes!)
* Documentation enhancements (lots!)

Version 0.2.0 Experimental (2023-05-30)
=======================================
Incomplete release caused by premature merge of development branch with
master. Oops.

Version 0.1.0 Experimental (2023-02-03)
=======================================
Getting ready for limited private test and evaluation. Logic is complete,
ConformU passes, docs are extensive, and there are templates for all
ASCOM device types. No end to documentation though ha ha.

