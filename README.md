# pyedbglib
pyedbglib is a collection of tools to talk to Microchip CMSIS-DAP based debuggers.
Build it, install it, and use it with various application scripts to interact with xEDBG debuggers.

## Disclaimer
Most testing has been done using nEDBG, although in theory the same API works on all xEDBG variants. 

## TLDR
Examples of how to install pyedbglib in development mode and lint are shown in the Makefile

## Development
To develop in this code base, use pip to install the code base in editable mode:
~~~~
pip install -e .[dev]
~~~~

* This will install a "symlink" in pythons path to your GIT repository so the code can be imported as:
import pyedbglib

The [dev] clause tells python to install development dependencies defined in setup.py, as well as regular dependencies.

## Lint
This project uses pylint to lint the code.

http://pylint.readthedocs.io/en/latest/

The linter is invoked with:
~~~~
pylint pyedbglib
~~~~

All contributions are expected to be respectably clean.
