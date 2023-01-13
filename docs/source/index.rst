.. image:: alpaca128.png
    :height: 92px
    :width: 128px
    :align: right

========================
Welcome to Alpyca Device
========================

This document describes the Alpyca Device project, a lightweight sample of
an Alpaca device driver. While meant to serve as a template, this sample
is actually a fully functional Alpaca Rotator simulator which passes the
|conformu| tests.

The idea here is to provide you, the prospective Alpaca device driver author,
with the code structure and boiler-plate code needed. By starting with this
project, you will see how to use the |falcon| in conjunction with
the built-in |wsgiref| to handle each of the REST endpoints
needed to implement a fully functional conforming Alpaca device. In addition,
you will see how to handle exceptions the correct way, including mapping
Python run-time errors into the Alpaca Exception response.

.. Tip::
    **Start Here:** :doc:`introduction`

.. Note::
    This is the 0.1.x developmental version. For release notes see
    |changes| on the |github|.

For background see |about| on the |ascsite|. As an astronomy developer
wanting to use Alpaca, we suggest you look over |devhelp| and join
the |supforum|.


.. |changes| raw:: html

    <a href="https://github.com/BobDenny/alpyca-device/blob/master/CHANGES.rst" target="_blank">
    the CHANGES document</a> (external)

.. |github| raw:: html

    <a href="https://github.com/BobDenny/alpyca-device" target="_blank">
    Alpyca Device GitHub repository</a>

.. |ascsite| raw:: html

    <a href="https://ascom-standards.org/index.htm" target="_blank">
    ASCOM Initiative web site</a> (external)

.. |about| raw:: html

    <a href="https://ascom-standards.org/About/Index.htm" target="_blank">
    About Alpaca and ASCOM</a> (external)

.. |conformu| raw:: html

    <a href="https://github.com/ASCOMInitiative/ConformU/releases" target="_blank">
    Conform Universal Test Tool</a> (external)

.. |falcon| raw:: html

    <a href="https://falcon.readthedocs.io/en/stable/" target="_blank">
    Falcon Web Framework</a> (external)

.. |wsgiref| raw:: html

    <a href="https://docs.python.org/3/library/wsgiref.html" target="_blank">
    Python wsgiref HTTP server</a> (external)

.. |devhelp| raw:: html

    <a href="https://ascom-standards.org/AlpacaDeveloper/Index.htm" target="_blank">
    Alpaca Developers Info</a> (external)

.. |supforum| raw:: html

    <a href="https://ascomtalk.groups.io/g/Developer" target="_blank">
    ASCOM Driver and Application Development Support Forum</a> (external)


.. toctree::
    :maxdepth: 2

    introduction
    roadmap
    faq
    modules


.. only:: html

    Indices and tables
    ==================

    * :ref:`genindex`
    * :ref:`modindex`
    * :ref:`search`
