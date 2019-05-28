"""
Implements Avr8 Protocol, a sub-protocol in the JTAGICE3 family of protocols.
"""
import logging
from .jtagice3protocol import Jtagice3Protocol
from .avr8protocolerrors import AVR8_ERRORS
from ..util import binary


class Avr8Protocol(Jtagice3Protocol):
    """
    Implements AVR8 protocol functionality on the JTAGICE3 protocol family
    """

    CMD_AVR8_QUERY = 0x00  # //! Capability discovery
    CMD_AVR8_SET = 0x01  # //! Set parameters
    CMD_AVR8_GET = 0x02  # //! Get parameters
    CMD_AVR8_ACTIVATE_PHYSICAL = 0x10  # //! Connect physically
    CMD_AVR8_DEACTIVATE_PHYSICAL = 0x11  # //! Disconnect physically
    CMD_AVR8_GET_ID = 0x12  # //! Read the ID
    CMD_AVR8_ATTACH = 0x13  # //! Attach to OCD module
    CMD_AVR8_DETACH = 0x14  # //! Detach from OCD module
    CMD_AVR8_PROG_MODE_ENTER = 0x15  # //! Enter programming mode
    CMD_AVR8_PROG_MODE_LEAVE = 0x16  # //! Leave programming mode
    CMD_AVR8_DISABLE_DEBUGWIRE = 0x17  # //! Disable debugWIRE interface
    CMD_AVR8_ERASE = 0x20  # //! Erase the chip
    CMD_AVR8_MEMORY_READ = 0x21  # //! Read memory
    CMD_AVR8_MEMORY_READ_MASKED = 0x22  # //! Read memory while via a mask
    CMD_AVR8_MEMORY_WRITE = 0x23  # //! Write memory
    CMD_AVR8_CRC = 0x24  # //! Calculate CRC
    CMD_AVR8_RESET = 0x30  # //! Reset the MCU
    CMD_AVR8_STOP = 0x31  # //! Stop the MCU
    CMD_AVR8_RUN = 0x32  # //! Resume execution
    CMD_AVR8_RUN_TO_ADDRESS = 0x33  # //! Resume with breakpoint
    CMD_AVR8_STEP = 0x34  # //! Single step
    CMD_AVR8_PC_READ = 0x35  # //! Read PC
    CMD_AVR8_PC_WRITE = 0x36  # //! Write PC
    CMD_AVR8_HW_BREAK_SET = 0x40  # //! Set breakpoints
    CMD_AVR8_HW_BREAK_CLEAR = 0x41  # //! Clear breakpoints
    CMD_AVR8_SW_BREAK_SET = 0x43  # //! Set software breakpoints
    CMD_AVR8_SW_BREAK_CLEAR = 0x44  # //! Clear software breakpoints
    CMD_AVR8_SW_BREAK_CLEAR_ALL = 0x45  # //! Clear all software breakpoints
    CMD_AVR8_PAGE_ERASE = 0x50  # //! Erase page

    RSP_AVR8_OK = 0x80  # //! All OK
    RSP_AVR8_LIST = 0x81  # //! List of items returned
    RSP_AVR8_DATA = 0x84  # //! Data returned
    RSP_AVR8_PC = 0x83  # //! PC value returned
    RSP_AVR8_FAILED = 0xA0  # //! Command failed to execute

    AVR8_FAILURE_INVALID_PHYSICAL_STATE = 0x31

    EVT_AVR8_BREAK = 0x40
    EVT_AVR8_IDR = 0x41

    AVR8_CTXT_CONFIG = 0x00  # //! Configuration
    AVR8_CTXT_PHYSICAL = 0x01  # //! Physical interface related
    AVR8_CTXT_DEVICE = 0x02  # //! Device specific settings
    AVR8_CTXT_OPTIONS = 0x03  # //! Option-related settings
    AVR8_CTXT_SESSION = 0x04  # //! Session-related settings

    AVR8_CONFIG_VARIANT = 0x00  # //! Device family/variant
    AVR8_CONFIG_FUNCTION = 0x01  # //! Functional intent

    AVR8_PHY_INTERFACE = 0x00  # //! Physical interface selector
    AVR8_PHY_JTAG_DAISY = 0x01  # //! JTAG daisy chain settings
    AVR8_PHY_DW_CLK_DIV = 0x10  # //! debugWIRE clock divide ratio
    AVR8_PHY_MEGA_PRG_CLK = 0x20  # //! Clock for programming megaAVR
    AVR8_PHY_MEGA_DBG_CLK = 0x21  # //! Clock for debugging megaAVR
    AVR8_PHY_XM_JTAG_CLK = 0x30  # //! JTAG clock for AVR XMEGA
    AVR8_PHY_XM_PDI_CLK = 0x31  # //! PDI clock for AVR XMEGA/TinyX

    AVR8_OPT_RUN_TIMERS = 0x00  # //! Keep timers running when stopped
    AVR8_OPT_DISABLE_DBP = 0x01  # //! No data breaks during reset
    AVR8_OPT_ENABLE_IDR = 0x03  # //! Relay IDR messages
    AVR8_OPT_POLL_INT = 0x04  # //! Configure polling speed
    AVR8_OPT_POWER_NAP = 0x05  # //! Use Power Nap
    AVR8_OPT_12V_UPDI_ENABLE = 0x06  # //! Enable UPDI using 12V
    AVR8_OPT_CHIP_ERASE_TO_ENTER = 0x07  # //! Use CHIP ERASE KEY when next entering programming mode

    AVR8_VARIANT_LOOPBACK = 0x00  # //! Dummy device
    AVR8_VARIANT_TINYOCD = 0x01  # //! tinyAVR or megaAVR with debugWIRE
    AVR8_VARIANT_MEGAOCD = 0x02  # //! megaAVR with JTAG
    AVR8_VARIANT_XMEGA = 0x03  # //! AVR XMEGA
    AVR8_VARIANT_TINYX = 0x05  # //! New AVR devices have UPDI interface
    AVR8_VARIANT_NONE = 0xFF  # //! No device

    AVR8_FUNC_NONE = 0x00  # //! Not configured
    AVR8_FUNC_PROGRAMMING = 0x01  # //! I want to program only
    AVR8_FUNC_DEBUGGING = 0x02  # //! I want a debug session

    AVR8_PHY_INTF_NONE = 0x00  # //! Not configured
    AVR8_PHY_INTF_JTAG = 0x04  # //! JTAG
    AVR8_PHY_INTF_DW = 0x05  # //! debugWIRE
    AVR8_PHY_INTF_PDI = 0x06  # //! PDI
    AVR8_PHY_INTF_PDI_1W = 0x08  # //! UPDI

    UPDI_12V_NONE = 0x00
    UPDI_12V_SIMPLE_PULSE = 0x01
    UPDI_12V_OWN_POWER_TOGGLE = 0x02
    UPDI_12V_USER_POWER_TOGGLE = 0x03

    AVR8_MEMTYPE_SRAM = 0x20
    AVR8_MEMTYPE_EEPROM = 0x22
    AVR8_MEMTYPE_SPM = 0xA0
    AVR8_MEMTYPE_FLASH_PAGE = 0xB0
    AVR8_MEMTYPE_EEPROM_PAGE = 0xB1
    AVR8_MEMTYPE_FUSES = 0xB2
    AVR8_MEMTYPE_LOCKBITS = 0xB3
    AVR8_MEMTYPE_SIGNATURE = 0xB4
    AVR8_MEMTYPE_OSCCAL = 0xB5
    AVR8_MEMTYPE_REGFILE = 0xB8
    AVR8_MEMTYPE_APPL_FLASH = 0xC0
    AVR8_MEMTYPE_BOOT_FLASH = 0xC1
    AVR8_MEMTYPE_APPL_FLASH_ATOMIC = 0xC2
    AVR8_MEMTYPE_BOOT_FLASH_ATOMIC = 0xC3
    AVR8_MEMTYPE_EEPROM_ATOMIC = 0xC4
    AVR8_MEMTYPE_USER_SIGNATURE = 0xC5
    AVR8_MEMTYPE_CALIBRATION_SIGNATURE = 0xC6
    AVR8_MEMTYPE_SIB = 0xD3

    ERASE_CHIP = 0x00
    ERASE_APP = 0x01
    ERASE_BOOT = 0x02
    ERASE_EEPROM = 0x03
    ERASE_APP_PAGE = 0x04
    ERASE_BOOT_PAGE = 0x05
    ERASE_EEPROM_PAGE = 0x06
    ERASE_USERSIG = 0x07

    def __init__(self, transport):
        self.logger = logging.getLogger(__name__)
        super(Avr8Protocol, self).__init__(
            transport, Jtagice3Protocol.HANDLER_AVR8_GENERIC)

    def error_as_string(self, code):
        """
        Get the response error as a string (error code translated to descriptive string)
        :return: error code as descriptive string
        """
        return AVR8_ERRORS[code]

    # Configuration shortcuts for AVR8 target types
    def set_variant(self, variant):
        """
        Sets the variant field in the config context
        :param variant: type of device
        """
        self.set_byte(self.AVR8_CTXT_CONFIG, self.AVR8_CONFIG_VARIANT, variant)

    def set_function(self, debugger_function):
        """
        Sets the function field in the config context
        :param debugger_function: function of this session (prog / debug)
        :return:
        """
        self.set_byte(self.AVR8_CTXT_CONFIG, self.AVR8_CONFIG_FUNCTION, debugger_function)

    def set_interface(self, interface):
        """
        Sets the function field in the physical context
        :param interface: physical interface setting
        """
        self.set_byte(self.AVR8_CTXT_PHYSICAL, self.AVR8_PHY_INTERFACE, interface)

    def write_device_data(self, data):
        """
        Write device info into the device context
        :param data: device data content
        """
        self._set_protocol(self.AVR8_CTXT_DEVICE, 0x00, data)

    def configure_daisy_chain(self, settings):
        """
        Sets the daisy-chain fields in the physical context
        :param settings: array of daisy-chain info
        """
        self._set_protocol(self.AVR8_CTXT_PHYSICAL, self.AVR8_PHY_JTAG_DAISY,
                           [0x04, settings[0], settings[1], settings[2], settings[3]])

    # Physical / connection commands
    def activate_physical(self, use_reset=False):
        """
        Activates the physical interface
        :param use_reset: reset
        :return:
        """
        self.logger.debug("Activate physical")
        # try:
        device_id = self.check_response(self.jtagice3_command_response(
            bytearray([self.CMD_AVR8_ACTIVATE_PHYSICAL, self.CMD_VERSION0, int(use_reset)])))

        # No ID returned is also ok (some interfaces are just not clever enough)
        if not device_id:
            self.logger.debug("ID=%02X%02X%02X%02X", device_id[3], device_id[2], device_id[1], device_id[0])
        return device_id

    def deactivate_physical(self):
        """
        Deactivates the physical interface
        """
        self.logger.debug("Deactivate physical")
        self.check_response(self.jtagice3_command_response(bytearray([self.CMD_AVR8_DEACTIVATE_PHYSICAL,
                                                                      self.CMD_VERSION0])))

    # Programming mode entry / exit commands
    def enter_progmode(self):
        """
        Enters programming mode
        """
        self.logger.debug("Enter prog mode")
        self.check_response(self.jtagice3_command_response(bytearray([self.CMD_AVR8_PROG_MODE_ENTER,
                                                                      self.CMD_VERSION0])))

    def leave_progmode(self):
        """
        Exits programming mode
        """
        self.logger.debug("Leave prog mode")
        self.check_response(self.jtagice3_command_response(bytearray([self.CMD_AVR8_PROG_MODE_LEAVE,
                                                                      self.CMD_VERSION0])))

    def get_id(self):
        """
        Reads the device ID
        :return: device ID
        """
        self.logger.debug("%s::get ID", self.__class__.__name__)
        return self.check_response(self.jtagice3_command_response(bytearray([self.CMD_AVR8_GET_ID, self.CMD_VERSION0])))

    # Debug mode entry / exit commands
    def attach(self, do_break=False):
        """
        Attaches the debugger to the target
        :param do_break: break execution on attach?
        """
        self.logger.debug("Attach")
        self.check_response(self.jtagice3_command_response(bytearray([self.CMD_AVR8_ATTACH, self.CMD_VERSION0,
                                                                      int(do_break)])))

    def detach(self):
        """
        Detaches the debugger from the target
        """
        self.logger.debug("Detach")
        self.check_response(self.jtagice3_command_response(bytearray([self.CMD_AVR8_DETACH, self.CMD_VERSION0])))

    # General memory access commands

    def erase(self, mode=0, address=0):
        """
        Erase target flash
        :param mode: flash erase mode to use
        :param address: start address to erase from
        """
        return self.check_response(self.jtagice3_command_response(
            bytearray([self.CMD_AVR8_ERASE, self.CMD_VERSION0, mode]) + binary.pack_le32(address)))

    def memory_read(self, memtype, address, num_bytes):
        """
        Read memory form the target
        :param memtype: memory type (section)
        :param address: start address
        :param num_bytes: number of bytes
        :return: memory read
        """
        self.logger.debug("Reading memory...")
        return self.check_response(self.jtagice3_command_response(
            bytearray([self.CMD_AVR8_MEMORY_READ, self.CMD_VERSION0, memtype]) +
            binary.pack_le32(address) + binary.pack_le32(num_bytes)))

    def memory_write(self, memtype, address, data):
        """
        Write memory to target
        :param memtype: memory type / region to access
        :param address: start address
        :param data: data to write
        """
        data = bytearray(data)
        return self.check_response(self.jtagice3_command_response(
            bytearray([self.CMD_AVR8_MEMORY_WRITE, self.CMD_VERSION0, memtype]) + binary.pack_le32(
                address) + binary.pack_le32(len(data)) + bytearray([0x00]) + data))

    # Debugging flow-control functions

    def reset(self):
        """
        Resets the core and holds it in reset
        """
        self.logger.debug("AVR core reset")
        self.check_response(self.jtagice3_command_response(bytearray([self.CMD_AVR8_RESET, self.CMD_VERSION0, 0x01])))

    def step(self):
        """
        Executes a single-step on the core.  A BREAK even will be generated when it has completed.
        This behaviour originates from previous debuggers which could do C level stepping which took time.
        """
        self.logger.debug("AVR core step")
        self.check_response(
            self.jtagice3_command_response(bytearray([self.CMD_AVR8_STEP, self.CMD_VERSION0, 0x01, 0x01])))

    def stop(self):
        """
        Requests a core halt.  A BREAK even will be generated when it has successfully stopped.
        """
        self.logger.debug("AVR core halt request")
        self.check_response(self.jtagice3_command_response(bytearray([self.CMD_AVR8_STOP, self.CMD_VERSION0, 0x01])))

    def run(self):
        """
        Resumes core execution
        """
        self.logger.debug("AVR core resume")
        self.check_response(self.jtagice3_command_response(bytearray([self.CMD_AVR8_RUN, self.CMD_VERSION0])))

    def run_to(self, address):
        """
        Runs to the given address.  A BREAK event will be generated when/if it reaches the address.
        :param address:
        """
        self.logger.debug("AVR core run to address")
        self.check_response(self.jtagice3_command_response(
            bytearray([self.CMD_AVR8_RUN_TO_ADDRESS, self.CMD_VERSION0]) + binary.pack_le32(address)))

    # Debug memory access functions

    def program_counter_read(self):
        """
        Reads out the program counter
        :return: PC value
        """
        program_counter = binary.unpack_le32(self.check_response(
            self.jtagice3_command_response(bytearray([self.CMD_AVR8_PC_READ, self.CMD_VERSION0])), self.RSP_AVR8_PC))
        msg = "PC read as 0x{:08X}".format(program_counter)
        self.logger.debug(msg)
        return program_counter

    def program_counter_write(self, program_counter):
        """
        Writes the program counter
        :param program_counter:
        """
        self.check_response(self.jtagice3_command_response(
            bytearray([self.CMD_AVR8_PC_WRITE, self.CMD_VERSION0]) + binary.pack_le32(program_counter)))

    def regfile_read(self):
        """
        Reads out the AVR register file (R0::R31)
        :return:
        """
        self.logger.debug("Reading register file")
        data = self.memory_read(self.AVR8_MEMTYPE_REGFILE, 0, 32)
        self.logger.debug(data)
        return data

    def regfile_write(self, data):
        """
        Writes the AVR registe file (R0::R31)
        :param data: register array
        :return:
        """
        if len(data) != 32:
            raise Exception("Invalid data length for regfile")
        self.logger.debug("Writing register file")
        return self.memory_write(self.AVR8_MEMTYPE_REGFILE, 0, data)

    # Software breakpoint functions

    def software_breakpoint_set(self, address):
        """
        Insert a software breakpoint at the given address
        :param address: breakpoint address
        """
        self.logger.debug("Set SWBP")
        self.check_response(self.jtagice3_command_response(
            bytearray([self.CMD_AVR8_SW_BREAK_SET, self.CMD_VERSION0]) + binary.pack_le32(address)))

    def software_breakpoint_clear(self, address):
        """
        Removes a software breakpoint from the given address
        :param address: breakpoint address
        """
        self.logger.debug("Clear SWBP")
        self.check_response(self.jtagice3_command_response(
            bytearray([self.CMD_AVR8_SW_BREAK_CLEAR, self.CMD_VERSION0]) + binary.pack_le32(address)))

    def software_breakpoint_clear_all(self):
        """
        Clears all software breakpoints
        """
        self.logger.debug("SWBP clear all")
        self.check_response(
            self.jtagice3_command_response(bytearray([self.CMD_AVR8_SW_BREAK_CLEAR_ALL, self.CMD_VERSION0])))
