"""
Implements an mEDBG-specific subset of the EDBG Protocol, a sub-protocol in the JTAGICE3 family of protocols.
"""
import logging
from .jtagice3protocol import Jtagice3Protocol


class mEdbgProtocol(Jtagice3Protocol):
    """
    Implements [m]EDBG protocol functionality on the JTAGICE3 protocol family
    """

    CMD_EDBG_QUERY = 0x00  # //! Capability discovery
    CMD_EDBG_SET = 0x01  # //! Set parameters
    CMD_EDBG_GET = 0x02  # //! Get parameters

    RSP_EDBG_OK = 0x80  # //! All OK
    RSP_EDBG_LIST = 0x81  # //! List of items returned
    RSP_EDBG_DATA = 0x84  # //! Data returned
    RSP_EDBG_FAILED = 0xA0  # //! Command failed to execute

    # Interesting config registers
    CONFIG_REG_SUFFER_BANK = 1
    CONFIG_REG_SUFFER_OFFSET = 0x20

    def __init__(self, transport):
        self.logger = logging.getLogger(__name__)
        super(mEdbgProtocol, self).__init__(
            transport, Jtagice3Protocol.HANDLER_EDBG)

    def read_config(self, bank, offset, length):
        """
        Reads bytes from config
        :param bank: 512b bank to read
        :param offset: offset within that bank
        :param length: number of values to read
        """

        self.logger.debug("mEDBG::read_config")
        response = self.jtagice3_command_response(
            bytearray([self.CMD_EDBG_GET, 0, bank+0x10, offset, length]))
        return self.peel_response(response, 0x84)

    def write_config(self, bank, offset, data):
        """
        Writes bytes to config
        :param bank: 512b bank to write
        :param offset: offset within that bank
        :param data: bytearray of values to write
        """
        if len(data) > 32:
            raise Exception("Unable to write >32  bytes!")
        self.logger.debug("mEDBG::write_config")
        response = self.jtagice3_command_response(
            bytearray([self.CMD_EDBG_SET, 0, bank+0x10, offset, len(data)])+data)
        return self.check_response(response)
