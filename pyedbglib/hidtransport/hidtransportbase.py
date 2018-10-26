"""
Base class for all HID transport mechanisms.
"""
import logging
from . import toolinfo


class CmsisDapDebugger(object):
    """
    Holds transport and DAP properties of a CMSIS-DAP debugger.
    Used to select the debugger to use if multiple debuggers are connected.
    """

    # pylint: disable=too-many-instance-attributes
    # These are primary keys used to identify the debugger.

    def __init__(self, vendor_id, product_id, serial_number, product_string=""):
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(logging.NullHandler())
        self.interface_number = -1
        self.vendor_id = vendor_id
        self.product_id = product_id
        self.serial_number = serial_number
        self.product_string = product_string
        self.firmware_version = ""
        self.device_vendor_id = ""
        self.device_name = ""
        self.packet_size = 64

    def set_packet_size(self, packet_size):
        """
        Sets the packet size
        :param packet_size: bytes per packet
        """
        self.packet_size = packet_size

    def set_product_string(self, product_string):
        """
        Sets the product string
        :param product_string: product name string
        """
        self.product_string = product_string


class HidTransportBase(object):
    """
    Base class for HID transports
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(logging.NullHandler())
        self.devices = []
        self.device = None
        self.detect_devices()

    def detect_devices(self):
        """
        Raise error as this method needs to be overridden.
        """
        raise NotImplementedError("method needs to be defined by sub-class")

    def connect(self, serial_number=None, product=None):
        """
        Makes a HID connection to a debugger
        :param serial_number: instance serial number to connect to
        :param product: product type to connect to
        :return:
        """
        # Support systems which use an empty-string as the standard for a unspecified USB serial
        if serial_number == '':
            serial_number = None

        device_count = len(self.devices)
        self.logger.debug("{:d} devices available".format(device_count))
        if device_count == 0:
            raise Exception("No CMSIS-DAP devices found.")

        matching_devices = 0
        selected_device = 0

        # TODO: this section should be refactored to have fewer branches and be more systematic

        # No product or serial number specified
        if serial_number is None and product is None:
            matching_devices = device_count
            if device_count == 1:
                selected_device = 0
        else:
            self.logger.debug("Looking for a match in {0:d} units".format(device_count))
            i = 0
            for device in self.devices:
                # Match both product and serial number
                if serial_number is not None and product is not None:
                    if device.serial_number == serial_number and device.product_string.upper().startswith(
                            product.upper()):
                        selected_device = i
                        matching_devices += 1
                # Look for product type if serial is not specified
                elif serial_number is None and product is not None:
                    self.logger.debug("> {:s}".format(device.product_string))
                    if device.product_string.upper().startswith(product.upper()):
                        selected_device = i
                        matching_devices += 1
                # Look for serial number if product is not specified
                elif product is None and serial_number is not None:
                    if device.serial_number == serial_number:
                        selected_device = i
                        matching_devices += 1
                # Something is horribly wrong
                else:
                    return False
                i += 1

        # Did we find exactly 1 tool?
        if matching_devices != 1:
            log_str = "Found {:d} daps matching the filter serial = \"{}\" and product = \"{}\""
            self.logger.debug(log_str.format(matching_devices, serial_number, product))
            if matching_devices > 1:
                self.logger.error("Too many products found. Please specify one of:")
                for device in self.devices:
                    self.logger.error(" > {:s} {:s}".format(device.product_string,
                                                            device.serial_number))
            return False

        # Everything is peachy, connect to the tool
        self.device = self.devices[selected_device]
        self.hid_connect(self.device)
        self.logger.debug("Connected OK")
        packet_size = toolinfo.get_default_report_size(self.device.product_id)
        self.device.set_packet_size(packet_size)
        self.hid_info()
        return True

    def disconnect(self):
        """
        Release the HID connection
        :return:
        """
        self.hid_disconnect()

    def hid_connect(self, device):
        """
        Raise error as this method needs to be overridden.
        """
        raise NotImplementedError("method needs to be defined by sub-class")

    def hid_info(self):
        """
        Raise error as this method needs to be overridden.
        """
        raise NotImplementedError("method needs to be defined by sub-class")

    def hid_disconnect(self):
        """
        Raise error as this method needs to be overridden.
        """
        raise NotImplementedError("method needs to be defined by sub-class")

    def get_report_size(self):
        """
        Get the packet size in bytes
        :return: bytes per packet/report
        """
        return self.device.packet_size
