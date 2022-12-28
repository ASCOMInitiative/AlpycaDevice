..
    The rinohtype PDF builder I use chokes on right-justified images
    failing to wrap them with the text. It also chokes on the |xxx|
    format hyperlinks to externals that I use for opening in a separate
    tab. Therefore I have html and rinoh conditionals in these docs (typ)
    Don't ask me why I had to repeat the main title for html and rinoh
    separately....

.. only:: html

    .. image:: alpaca128.png
        :height: 92px
        :width: 128px
        :align: right

    ========================
    Welcome to Alpyca Device
    ========================

.. only:: rinoh or rst

    ========================
    Welcome to Alpyca Device
    =========================

This document describes the Alpyca Device project, a lightweight sample of
an Alpaca device driver. While meant to serve as a template, this sample
is actually a fully functional Alpaca Rotator simulator which passes the 
Conform Universal tests. 

The idea here is to provide you, the prospective Alpaca device driver author,
with the code structure and boiler-plate code needed. By starting with this
project, you will see how to use the Falcon REST processor in conjunction with
the built-in Python wsgiref HTTP server to handle each of the REST endpoints
needed to implement a fully functional conforming Alopaca device. In addition,
you will see how to handle exceptions the correct way, including mapping 
Python run-time errors into the Alpaca Exception response. 

.. only:: html

    For example, the same code can be used to control any ASCOM-compatible
    telescope. This includes not only telescopes that are controlled with
    classic ASCOM/COM on a Windows machine, but also any telescopes which
    are *not* connected to a Windows machine, but instead speak Alpaca
    natively. The Windows |remote| gives an Alpaca interface to any
    Windows-resident device, allowing you to use the device via this library
    from any platform on the net or local host.

    .. Tip::
        **Start Here:** :doc:`introduction`

    .. Note::
        This is version 2.0.3 the second production release. For release notes see
        |changes| on the |github|.

    For background see |about| on the |ascsite|. As an astronomy developer
    wanting to use Alpaca, we suggest you look over |devhelp| and join
    the |supforum|.

    .. Attention::
        Alpaca is not dependent on Windows. See |about|.

.. only:: rinoh or rst

    For example, the same code can be used to control any ASCOM-compatible
    telescope. This includes not only telescopes that are controlled with
    classic ASCOM/COM on a Windows machine, but also any telescopes which
    are *not* connected to a Windows machine, but instead speak Alpaca
    natively. The Windows
    `ASCOM Remote middleware <https://github.com/ASCOMInitiative/ASCOMRemote/releases>`_
    gives an Alpaca interface to any Windows-resident device, allowing you
    to use the device via this library from any platform on the net or
    local host.

    .. Tip::
        **Start Here:** :doc:`introduction`

    .. Note::
        This is version 2.0.3, the second production release. For release notes see
        `the CHANGES document <https://github.com/ASCOMInitiative/alpyca/blob/master/CHANGES.rst>`_
        on the `Alpyca GitHub repository <https://github.com/ASCOMInitiative/alpyca>`_.

   For background see
    `About Alpaca and ASCOM <https://ascom-standards.org/About/Index.htm>`_
    on the
    `ASCOM Initiative web site <https://ascom-standards.org/index.htm>`_.
    As an astronomy developer wanting to use Alpaca, we suggest
    you look over
    `Alpaca Developers Info <https://ascom-standards.org/AlpacaDeveloper/Index.htm>`_ and join the
    `ASCOM Driver and Application Development Support Forum <https://ascomtalk.groups.io/g/Developer>`_.

    .. Attention::
        Alpaca is not dependent on Windows! See `About Alpaca and ASCOM <https://ascom-standards.org/About/Index.htm>`_.

.. |changes| raw:: html

    <a href="https://github.com/ASCOMInitiative/alpyca/blob/master/CHANGES.rst" target="_blank">
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

.. |remote| raw:: html

    <a href="https://github.com/ASCOMInitiative/ASCOMRemote/releases" target="_blank">
    ASCOM Remote middleware</a> (external)

.. |devhelp| raw:: html

    <a href="https://ascom-standards.org/AlpacaDeveloper/Index.htm" target="_blank">
    Alpaca Developers Info</a> (external)

.. |supforum| raw:: html

    <a href="https://ascomtalk.groups.io/g/Developer" target="_blank">
    ASCOM Driver and Application Development Support Forum</a> (external)


.. toctree::
    :maxdepth: 2

    introduction

    faq

.. only:: html

    Indices and tables
    ==================

    * :ref:`genindex`
    * :ref:`modindex`
    * :ref:`search`
