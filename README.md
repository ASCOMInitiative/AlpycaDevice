# AlpycaDevice - Python Alpaca Device Framework and Templates

<img align="right" width="210" height="166" hspace="20" vspace="20" src="https://ascom-standards.org/alpyca/readme-assets/AlpacaLogo210.png">

This project is a lightweight Python framework for a device
driver that supports the Alpaca protocol and ASCOM Standards. It implements
a basic Rotator device with a simple simulation for Conform tests.
**Templates for all ASCOM device types are provided**. The "boiler plate" logic
remains the same for any device.

## Incomplete Update (May 31, 2023) *Incomplete - Needs templates and docs updated.* Result of premature merge of my development branch into the master. Oops. Will have this out by week's end

## 30-May-2023 Doc and Video are for 0.1, and 0.3 experimental is now on the master branch

## [Alpyca Device Full Documentation](https://ascom-standards.org/alpycadevice/)

## [Quick Start Video Introduction](https://www.youtube.com/watch?v=bJ-1TJBfe0c")

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
10. Now use the Alpaca Protocol Checker in ConformU to validate the

## Status of this project

Fairly extensive refactoring of bits to make supporting multiple device *types* as
well as multiple instandces of a given device type. Passes [Conform
Universal](https://github.com/ASCOMInitiative/ConformU#conform-universal) for
Rotator device, as well as [Conform
Universal](https://github.com/ASCOMInitiative/ConformU#conform-universal) Alpaca
Protocol tests.
docstrings and [Sphinx build to
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
