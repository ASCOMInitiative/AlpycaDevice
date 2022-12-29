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

.. only:: html

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

.. only:: rinoh or rst

    This document describes the Alpyca Device project, a lightweight sample of
    an Alpaca device driver. While meant to serve as a template, this sample
    is actually a fully functional Alpaca Rotator simulator which passes the
    `Conform Universal Test Tool <href="https://ascom-standards.org/About/Index.htm>`_
    tests.

    The idea here is to provide you, the prospective Alpaca device driver author,
    with the code structure and boiler-plate code needed. By starting with this
    project, you will see how to use the
    `Falcon Web Framework <href="https://falcon.readthedocs.io/en/stable/>`_
    in conjunction with
    the built-in
    `Python wsgiref HTTP server <href="https://docs.python.org/3/library/wsgiref.html>`_
    to handle each of the REST endpoints
    needed to implement a fully functional conforming Alpaca device. In addition,
    you will see how to handle exceptions the correct way, including mapping
    Python run-time errors into the Alpaca Exception response.

    .. Tip::
        **Start Here:** :doc:`introduction`

    .. Note::
        This is the 0.1.x developmental version. For release notes see
        `the CHANGES document <https://github.com/BobDenny/alpyca-device/blob/master/CHANGES.rst>`_
        on the `Alpyca Device GitHub repository <https://github.com/BobDenny/alpyca-device>`_.

    For background see
    `About Alpaca and ASCOM <https://ascom-standards.org/About/Index.htm>`_
    on the
    `ASCOM Initiative web site <https://ascom-standards.org/index.htm>`_.
    As an astronomy developer wanting to use Alpaca, we suggest
    you look over
    `Alpaca Developers Info <https://ascom-standards.org/AlpacaDeveloper/Index.htm>`_ and join the
    `ASCOM Driver and Application Development Support Forum <https://ascomtalk.groups.io/g/Developer>`_.

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

    faq

.. only:: html

    Indices and tables
    ==================

    * :ref:`genindex`
    * :ref:`modindex`
    * :ref:`search`
