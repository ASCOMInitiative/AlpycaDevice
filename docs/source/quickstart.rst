.. image:: alpaca128.png
    :height: 92px
    :width: 128px
    :align: right

=========================
Alpyca Device Quick Start
=========================

Here's how to get this sample running on your development system. We recommended
you use |vscode| for Python development but it's cerainly not a requirement.

1. Clone the |alpdev| from GitHub
2. The ``device`` folder has all of the driver app files, ``app.py`` is the startup
3. Look at ``config.toml`` and if port 5555 is ok, you can leave everything else for now.
4. Recommend you create (and activate) a separate Python virtual environment.
   You do not need Conda or any fancy virtual environment tools.
5. Use ``pip`` to install ``falcon`` and ``toml``. These are the only two packages
   needed by the driver sample.
6. If you don't have the |conformu|, get it now.
7. Start the sample/template from the ``device`` folder ``python app.py``. It will
   not write to the shell/stdout. See the rotator.log file created in the ``device``
   folder.
8. Start ConformU and click Select Device. The sample should be discovered. If your
   dev system is on multiple IP addresses, you'll see it listed multiple times.
   Pick any one.
9. Click Start and watch it exercise the sample device. After a while it  should
   complete successfully.


.. |vscode| raw:: html

    <a href="https://code.visualstudio.com/" target="_blank">
    Visual Studio Code</a>

.. |alpdev| raw:: html

    <a href="https://github.com/BobDenny/AlpycaDevice" target="_blank">
    AlpycaDevice repository</a>

.. |conformu| raw:: html

    <a href="https://github.com/ASCOMInitiative/ConformU/releases" target="_blank">
    Conform Universal Test Tool</a>
