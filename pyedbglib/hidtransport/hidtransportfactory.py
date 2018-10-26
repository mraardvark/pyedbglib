"""
Factory for HID transport connections.
Currently supports only Cython/HIDAPI
"""

import platform
import logging


def hid_transport(library="hidapi"):
    """
    Dispatch a transport layer for the OS in question
    """
    logger = logging.getLogger(__name__)
    logger.addHandler(logging.NullHandler())
    operating_system = platform.system().lower()
    logger.debug("HID transport using library '{:s}' on OS '{:s}'".format(library, operating_system))

    # HID API is the primary transport
    if library == 'hidapi':
        hid_api_supported_os = ['windows', 'darwin', 'linux', 'linux2']
        if operating_system in hid_api_supported_os:
            from .cyhidapi import CyHidApiTransport
            return CyHidApiTransport()

        msg = "System '{0:s}' not implemented for library '{1:s}'".format(operating_system, library)
        logger.error(msg)
        raise Exception(msg)

    # Other transports may include cmsis-dap DLL, atusbhid (dll or so) etc
    msg = "Transport library '{0}' not implemented.".format(library)
    logger.error(msg)
    raise Exception(msg)
