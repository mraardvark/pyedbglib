# pyedbglib
pyedbglib is a collection of tools to talk to Microchip CMSIS-DAP based debuggers.
Build it, install it, and use it with various application scripts to interact with xEDBG debuggers.

## Example usage
```python
# Import a transport provider
from pyedbglib.hidtransport.hidtransportfactory import hid_transport
# Import a protocol driver
from pyedbglib.protocols import housekeepingprotocol

# Create transport
transport = hid_transport()

# Connect to transport
transport.connect()

# Create protocol, passing in transport object
hk = housekeepingprotocol.Jtagice3HousekeepingProtocol(transport)
        
# Use protocol as you want
hk.start_session()
print("Version info:")
print(hk.read_version_info())
hk.end_session()
```

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
