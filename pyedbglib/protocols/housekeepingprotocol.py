"""
Implements Housekeeping Protocol, a sub-protocol in the JTAGICE3 family of protocols.
"""
import logging

from .jtagice3protocol import Jtagice3Protocol
from ..util import binary


class Jtagice3HousekeepingProtocol(Jtagice3Protocol):
    """
    Implements housekeeping functionality on the JTAGICE3 protocol family
    """

    # Query contexts
    HOUSEKEEPING_QUERY_COMMANDS = 0x00
    HOUSEKEEPING_QUERY_ANALOG_CHANNELS = 0x01
    HOUSEKEEPING_QUERY_SPECIAL_ABILITIES = 0x02

    # Protocol commands
    CMD_HOUSEKEEPING_START_SESSION = 0x10
    CMD_HOUSEKEEPING_END_SESSION = 0x11
    CMD_HOUSEKEEPING_FW_UPGRADE = 0x50

    # Get/Set contexts
    HOUSEKEEPING_CONTEXT_CONFIG = 0x00
    HOUSEKEEPING_CONTEXT_ANALOG = 0x01
    HOUSEKEEPING_CONTEXT_STATEMENT = 0x02
    HOUSEKEEPING_CONTEXT_USB = 0x03
    HOUSEKEEPING_CONTEXT_STATISTICS = 0x80
    HOUSEKEEPING_CONTEXT_DIAGNOSTICS = 0x81

    # Config context
    HOUSEKEEPING_CONFIG_HWREV = 0x00
    HOUSEKEEPING_CONFIG_FWREV_MAJ = 0x01
    HOUSEKEEPING_CONFIG_FWREV_MIN = 0x02
    HOUSEKEEPING_CONFIG_BUILD = 0x03
    HOUSEKEEPING_CONFIG_CHIP = 0x05
    HOUSEKEEPING_CONFIG_BLDR_MAJ = 0x06
    HOUSEKEEPING_CONFIG_BLDR_MIN = 0x07
    HOUSEKEEPING_CONFIG_DEBUG_BUILD = 0x08
    HOUSEKEEPING_CONFIG_FIRMWARE_IMAGE = 0x09

    # USB context
    HOUSEKEEPING_USB_MAX_READ = 0x00
    HOUSEKEEPING_USB_MAX_WRITE = 0x01
    HOUSEKEEPING_USB_EP_SIZE_HID = 0x10
    HOUSEKEEPING_USB_EP_SIZE_CDC = 0x11

    # Diagnostics
    HOUSEKEEPING_DIAGNOSTICS_RESET_CAUSE = 0x00
    HOUSEKEEPING_DIAGNOSTICS_BOD_CTRL = 0x01
    HOUSEKEEPING_HOST_ID = 0x02
    HOUSEKEEPING_HOST_REV = 0x03
    HOUSEKEEPING_MODULE_VER_JTAG = 0x04
    HOUSEKEEPING_MODULE_VER_AW = 0x05
    HOUSEKEEPING_DIAGNOSTICS_CPU_CLK = 0x06

    # Analog
    HOUSEKEEPING_ANALOG_VTREF = 0x00
    HOUSEKEEPING_ANALOG_VTG_BUF = 0x01
    HOUSEKEEPING_ANALOG_VUSB = 0x02
    HOUSEKEEPING_TSUP_VOLTAGE = 0x20

    def __init__(self, transport):
        super(Jtagice3HousekeepingProtocol, self).__init__(transport, Jtagice3Protocol.HANDLER_HOUSEKEEPING)
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(logging.NullHandler())
        self.logger.debug("Created AVR housekeeping protocol")

    def list_supported_commands(self):
        """
        Uses the query interface to list all supported commands
        """
        self.logger.debug("Querying commands supported by this instance of housekeeping handler")
        commands = self.query(self.HOUSEKEEPING_QUERY_COMMANDS)
        return commands

    # Direct protocol commands
    def start_session(self):
        """
        Starts a session with the debugger (sign-on)
        """
        self.logger.debug("Housekeeping::start_session")
        response = self.jtagice3_command_response(bytearray([self.CMD_HOUSEKEEPING_START_SESSION, self.CMD_VERSION0]))
        self.check_response(response)

    def end_session(self, reset_tool=False):
        """
        Ends a session with the debugger (sign-off)
        :param reset_tool: resets the hardware
        :return:
        """
        self.logger.debug("Housekeeping::end_session")
        response = self.jtagice3_command_response(
            bytearray([self.CMD_HOUSEKEEPING_END_SESSION, self.CMD_VERSION0, 1 if reset_tool else 0]))
        self.check_response(response)

    def enter_upgrade_mode(self, key=0x31727C10):
        """
        Puts the debugger into firmware upgrade mode
        :param key: upgrade key
        :return:
        """
        self.logger.debug("Housekeeping::enter_upgrade_mode")
        try:
            response = self.jtagice3_command_response(
                bytearray([self.CMD_HOUSEKEEPING_FW_UPGRADE, self.CMD_VERSION0]) + binary.pack_be32(key))
        except IOError:
            self.logger.debug("IOError on enter upgrade mode. Device rebooted before response was read.")
        else:
            self.check_response(response)

    def read_version_info(self):
        """
        Reads version info from the debugger
        """
        self.logger.debug("Housekeeping::reading version info")

        # Results in dict form
        versions = {
            # HW version
            'hardware': self.get_byte(self.HOUSEKEEPING_CONTEXT_CONFIG, self.HOUSEKEEPING_CONFIG_HWREV),
            # FW version
            'firmware_major': self.get_byte(self.HOUSEKEEPING_CONTEXT_CONFIG, self.HOUSEKEEPING_CONFIG_FWREV_MAJ),
            'firmware_minor': self.get_byte(self.HOUSEKEEPING_CONTEXT_CONFIG, self.HOUSEKEEPING_CONFIG_FWREV_MIN),
            'build': self.get_le16(self.HOUSEKEEPING_CONTEXT_CONFIG, self.HOUSEKEEPING_CONFIG_BUILD),
            # BLDR
            'bootloader': self.get_le16(self.HOUSEKEEPING_CONTEXT_CONFIG, self.HOUSEKEEPING_CONFIG_BLDR_MAJ),
            # Host info
            'chip': self.get_byte(self.HOUSEKEEPING_CONTEXT_CONFIG, self.HOUSEKEEPING_CONFIG_CHIP),
            'host_id': self.get_le32(self.HOUSEKEEPING_CONTEXT_CONFIG, self.HOUSEKEEPING_HOST_ID),
            'host_rev': self.get_byte(self.HOUSEKEEPING_CONTEXT_CONFIG, self.HOUSEKEEPING_HOST_REV),
            # Misc
            'debug': self.get_byte(self.HOUSEKEEPING_CONTEXT_CONFIG, self.HOUSEKEEPING_CONFIG_DEBUG_BUILD)
        }

        try:
            versions['fire'] = self.get_byte(self.HOUSEKEEPING_CONTEXT_CONFIG, self.HOUSEKEEPING_CONFIG_FIRMWARE_IMAGE)
        except IOError:
            versions['fire'] = None

        return versions
