.. image:: alpaca128.png
    :height: 92px
    :width: 128px
    :align: right

=========================
Alpyca Device Quick Start
=========================

Running the Sample with the Conformance Checker
------------------------------------------------

Here's how to get this sample running on your development system. We recommended
you use |vscode| for Python development but it's cerainly not a requirement.

1. Clone the |alpdev| from GitHub
2. The ``device`` folder has all of the driver app files, ``app.py`` is the
   startup
3. Look at ``config.toml`` and if port 5555 is ok, you can leave everything else
   for now.
4. Recommend you create (and activate) a separate Python virtual environment.
   You do not need Conda or any fancy virtual environment tools, just use an
   ``venv`` type.
5. Use ``pip`` to install ``falcon`` and ``toml``. These are the only two
   packages needed by the driver sample.
6. Start the sample/template from the ``device`` folder ``python app.py``. It
   will not write to the shell/stdout. See the rotator.log file created in the
   root folder.
7. Start ConformU and click Select Device. The sample should be discovered. If
   your dev system is on multiple IP addresses, you'll see it listed multiple
   times. Pick any one.
8. Click Start and watch it exercise the sample device. After a while it  should
   complete successfully.

Have a look through the code, step through it with the debugger, etc. If you
need more context have a look through the :doc:`/introduction`. Also keep in
mind that there are many resources at |devhelp| and the |supforum|

.. _create-first_driver:

Creating Your First Driver
--------------------------

OK, you have run the Rotator sample and maybe caught it in various places with
the debugger and maybe you've looked at the :doc:`introduction` and/or the
:doc:`roadmap`. Or not. Here's how to get started implementing your driver. Let's say
you want to make a roll-off roof driver.

1. The essential modules are all in the ``device`` folder.  Make a copy
   **outside the cloned GitHub tree**. This will serve as your driver project
   root.
2. Remove the ``rotator.py`` module from your driver project folder.
3. Copy the ``dome.py`` module from the ``templates`` folder into your project
   folder. Note that a roll-off roof is a type of dome in ASCOM (norotating
   part, only open-close).
4. Open the ``dome.py`` module.
5. Find the ``DomeMetadata`` class and edit it to reflect your dome's
   descriptive metadata. The ``##`` delimited sections elsewhere indicate things
   you need to supply in the ``dome.py`` module to  make it your own.
6. Open your project's ``app.py`` module.
7. Remove this line
      ``import rotator``
   replace with
      ``import dome``
8. Remove the following lines
      ``rotator.logger = logger                 # Hook the master logger``
      ``rotator.start_rot_device(logger)        # Start the physical device``
   replace with
      ``dome.logger = logger``
9. Remove the following line
      ``init_routes(falc_app, 'rotator', rotator)``
   replace with
      ``init_routes(falc_app, 'dome', dome)``
10. Open your project's ``management.py`` module
11. Remove this line
        ``from rotator import RotatorMetadata``
    replace with
        ``from dome import DomeMetadata``
12. Find  ``class configureddevices`` and change the references ``RotatorMetadata``
    to ``DomeMetadata``.
13. OK, that's all there is to assemble the pieces. If you were to go back to
    ``dome.py`` and replace the ``##`` stuff with calls to your device code or just
    stub it out so the app would run, you would have a driver that would be
    discoverable and the endpoint responders would be called when any app talks
    to your device.

.. |vscode| raw:: html

    <a href="https://code.visualstudio.com/" target="_blank">
    Visual Studio Code</a>

.. |alpdev| raw:: html

    <a href="https://github.com/BobDenny/AlpycaDevice" target="_blank">
    AlpycaDevice repository</a>

.. |conformu| raw:: html

    <a href="https://github.com/ASCOMInitiative/ConformU/releases" target="_blank">
    Conform Universal Test Tool</a>

.. |supforum| raw:: html

    <a href="https://ascomtalk.groups.io/g/Developer" target="_blank">
    ASCOM Driver and Application Development Support Forum</a>

.. |devhelp| raw:: html

    <a href="https://ascom-standards.org/AlpacaDeveloper/Index.htm" target="_blank">
    Alpaca Developers Info</a>


