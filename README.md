# AlpycaDevice (0.1.0) Python 3.7+ Alpaca Device Framework

<img align="right" width="210" height="166" hspace="20" vspace="20" src="https://ascom-standards.org/alpyca/readme-assets/AlpacaLogo210.png">
This project is a  lightweight framework for a device
driver that supports the Alpaca protocol and ASCOM Standards. It implements
a basic Rotator device that is structured in a way that the
Rotator-specific API endpoint implementations can be easily replaced with an
API endpoints implementation for any ASCOM device. The "boiler plate" logic
remains the same.

## [Alpyca Device Full Documentation](https://ascom-standards.org/alpycadevice/)

## Quick Start

Here's how to get this sample running on your development system. We recommended
you use [Visual Studio Code](https://code.visualstudio.com/) and the Python
plugins including the recommended linting tools (cross platform, Mac,
Linux, Windows) for Python development but it's certainly not a requirement.

1. Clone the [this repo](https://github.com/BobDenny/AlpycaDevice) from GitHub.
2. The ``device`` folder has all of the driver app files, ``app.py`` is the startup
3. Look at ``config.toml`` and if port 5555 is ok, you can leave everything else for now.
4. Recommend you create (and activate) a separate Python virtual environment.
   You do not need Conda or any fancy virtual environment tools.
5. Use ``pip`` to install ``falcon`` and ``toml``. These are the only two packages
   needed by the driver sample.
6. If you don't have the cross-platform
   [Conform Universal tool](https://github.com/ASCOMInitiative/ConformU/releases) get it now.
7. Start the sample/template from the ``device`` folder ``python app.py``. It will
   not write to the shell/stdout. See the ``rotator.log`` file created in the ``device``
   folder.
8. Start ConformU and click Select Device. The sample should be discovered. If your
   dev system is on multiple IP addresses, you'll see it listed multiple times.
   Pick any one.
9. Click Start and watch it exercise this sample device. After a while it should
   complete successfully.

## Status (Jan 2023) *Experimental - Limited Distribution*

Ready for initial testing by others. Passes [Conform
Universal](https://github.com/ASCOMInitiative/ConformU#conform-universal) for
Rotator device, docstrings and [Sphinx build to
HTML](https://ascom-standards.org/alpycadevice/) completed.

## Potential Applications

* **Self-contained** device (e.g. on Raspberry Pi etc) that can be used by native Alpaca
  speaking programs like [Cartes du Ciel](https://www.ap-i.net/skychart/en/start),
  [Sky Safari 7](https://skysafariastronomy.com/) (pro or plus),
  as well as Windows apps like
  [SGP](https://www.sequencegeneratorpro.com/),
  [NINA](https://nighttime-imaging.eu/),
  [ACP](https://acpx.dc3.com/), etc. that speak Windows ASCOM/COM
* Linux/Max/Windows driver for Windows apps like
  [SGP](https://www.sequencegeneratorpro.com/),
  [NINA](https://nighttime-imaging.eu/),
  [ACP](https://acpx.dc3.com/), etc. that
  speak Windows ASCOM/COM
* Linux/Mac/Windows driver for native Alpaca-speaking apps like
  [Sky Safari 7](https://skysafariastronomy.com/).
* Use this to make an Alpaca front end for an INDI device running on Linux or MacOS,
  and make that device usable from Windows programs as noted above.
* Use your imagination...

## How to get Support

Use the [ASCOM Driver and Application Development Support Forum](https://ascomtalk.groups.io/g/Developer).
