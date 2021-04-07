# pyedbglib (relocated)
This repo has been superseded by: https://github.com/microchip-pic-avr-tools/pyedbglib

pyedbglib is a low-level protocol library for communicating with Microchip CMSIS-DAP based debuggers

It can be installed using pip:
```
pip install pyedbglib
```

## Usage
pyedbglib does not provide any end-user functionality on its own.
It is implemented according to the "Atmel EDBG-based Tools Protocols" document although the code and the documentation may not always be in sync.
pyedbglib is intended to be used by Python applications communicating with Microchip target devices via Microchip CMSIS-DAP based debuggers.

The following Atmel/Microchip debuggers are supported:
* JTAGICE3 (only firmware version 3.x)
* Atmel-ICE
* Power Debugger
* EDBG
* mEDBG
* PKOB nano (nEDBG)
* MPLAB PICkit 4 In-Circuit Debugger (only when in 'AVR mode')
* MPLAB Snap In-Circuit Debugger (only when in 'AVR mode')

Not all debuggers support all protocols or functions within them.

## pyedbglib version
When pyedbglib is installed as a python package (pip install pyedbglib) the package will contain a version.py file with the version of the package:
```
from pyedbglib import version
print("pyedbglib version {}".format(version.VERSION))
```
Alternatively if several python packages are being used it would be best to give the version a specific name:
```
from pyedbglib.version import VERSION as pyedbglib_version
print("pyedbglib version {}".format(pyedbglib_version))
```

## Development
To develop in this code base, use pip to install the code base in editable mode:
```
pip install -e .[dev]
```

This will install a symlink in pythons path to your GIT repository so the code can be imported as:
```
import pyedbglib
```

The [dev] clause tells python to install development dependencies defined in setup.py, as well as regular dependencies.

## Lint
This project uses pylint to lint the code.

http://pylint.readthedocs.io/en/latest/

The linter is invoked with:
```
pylint pyedbglib
```

All contributions are expected to be respectably clean.

## Notes
#### Linux systems
HIDAPI needs to build using packages: libusb-1.0.0-dev, libudev-dev

Create udev rules for the debuggers:
```
Example udev rules file
Store in /etc/udev/rules.d

HIDAPI/libusb:

# JTAGICE3
SUBSYSTEM=="usb", ATTRS{idVendor}=="03eb", ATTRS{idProduct}=="2140", MODE="0666"
# Atmel-ICE
SUBSYSTEM=="usb", ATTRS{idVendor}=="03eb", ATTRS{idProduct}=="2141", MODE="0666"
# Power Debugger
SUBSYSTEM=="usb", ATTRS{idVendor}=="03eb", ATTRS{idProduct}=="2144", MODE="0666"
# EDBG - debugger on Xplained Pro
SUBSYSTEM=="usb", ATTRS{idVendor}=="03eb", ATTRS{idProduct}=="2111", MODE="0666"
# mEDBG - debugger on Xplained Mini
SUBSYSTEM=="usb", ATTRS{idVendor}=="03eb", ATTRS{idProduct}=="2145", MODE="0666"
# PKOB nano (nEDBG) - debugger on Curiosity Nano
SUBSYSTEM=="usb", ATTRS{idVendor}=="03eb", ATTRS{idProduct}=="2175", MODE="0666"
# MPLAB PICkit 4 In-Circuit Debugger
SUBSYSTEM=="usb", ATTRS{idVendor}=="03eb", ATTRS{idProduct}=="2177", MODE="0666"
# MPLAB Snap In-Circuit Debugger
SUBSYSTEM=="usb", ATTRS{idVendor}=="03eb", ATTRS{idProduct}=="2180", MODE="0666"
```
