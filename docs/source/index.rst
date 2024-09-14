.. image:: alpaca128.png
    :height: 92px
    :width: 128px
    :align: right

===============================
Welcome to the AlpycaDevice SDK
===============================

This document describes the AlpycaDevice SDK project, a lightweight working
sample of an Alpaca device driver with templates for all ASCOM device types. The
sample is actually a fully functional Alpaca Rotator simulator which passes the
|conformu| comprehensive |functest| and |prototest|. Dependencies are kept to an absolute
minimum.

The idea here is to provide you, the prospective Alpaca device driver author,
with the code structure and "boiler-plate" support code needed. **No interaction
with HTTP or JSON is needed**. Only two dependencies (and of course *their*
dependencies) are needed.

By starting with this project, you will be able to implement a fully functional
conforming Alpaca device with a minimum of "just in time learning".

.. Tip::
    **Start Here:** :doc:`/quickstart` then look through :doc:`/introduction`.

.. Note::
    This is the 1.0.0 (September, 2024) production version. This is the first
    release that contains the additions to the interfaces for Platform 7.
    See |plat7changes|. For Release Notes on this SDK see the
    |changes| on the |github|.

For background see |about| and |alpcon| on the |ascsite|. As an astronomy
developer wanting to use Alpaca, we suggest you look over |devhelp| and join the
|supforum|.


.. |changes| raw:: html

    <a href="https://github.com/ASCOMInitiative/AlpycaDevice/blob/master/CHANGES.rst" target="_blank">
    CHANGES document</a>

.. |github| raw:: html

    <a href="https://github.com/ASCOMInitiative/AlpycaDevice" target="_blank">
    Alpyca Device SDK GitHub repository</a>

.. |ascsite| raw:: html

    <a href="https://ascom-standards.org/index.htm" target="_blank">
    ASCOM Initiative web site</a>

.. |about| raw:: html

    <a href="https://ascom-standards.org/About/Index.htm" target="_blank">
    About Alpaca and ASCOM</a>

.. |alpcon| raw:: html

    <a href="https://ascom-standards.org/About/Conn-Alpaca.htm" target="_blank">
    ASCOM Alpaca Connectivity</a>

.. |conformu| raw:: html

    <a href="https://github.com/ASCOMInitiative/ConformU/releases" target="_blank">
    Conform Universal Test Tool</a>

.. |falcon| raw:: html

    <a href="https://falcon.readthedocs.io/en/stable/" target="_blank">
    Falcon Web Framework</a>

.. |wsgiref| raw:: html

    <a href="https://docs.python.org/3/library/wsgiref.html" target="_blank">
    Python wsgiref HTTP server</a>

.. |devhelp| raw:: html

    <a href="https://ascom-standards.org/AlpacaDeveloper/Index.htm" target="_blank">
    Alpaca Developers Info</a>

.. |supforum| raw:: html

    <a href="https://ascomtalk.groups.io/g/Developer" target="_blank">
    ASCOM Driver and Application Development Support Forum</a>

.. |functest| raw:: html

    <a href="https://raw.githubusercontent.com/BobDenny/AlpycaDevice/master/Current%20ConformU%20Validation.txt">
    function test</a>

.. |prototest| raw:: html

    <a href="https://raw.githubusercontent.com/BobDenny/AlpycaDevice/master/Current%20ConformU%20Protocol.txt" target="_blank">
    protocol tests</a>

.. |plat7changes| raw:: html

    <a href="https://ascom-standards.org/newdocs/relnotes.html" target="_blank">
    Release Notes for ASCOM Platform 7</a>

.. toctree::
    :maxdepth: 2

    quickstart
    introduction
    roadmap
    modules
    migrating
    vscode

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
