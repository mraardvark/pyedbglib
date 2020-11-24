"""HID transport layer based on Cython and Hidapi"""
import sys
try:
    import hid
except ImportError:
    MSG = "This transport class requires cython and hidapi to be installed:\r\n"
    MSG += "> pip install cython\r\n"
    MSG += "> pip install hidapi\r\n"
    raise ImportError(MSG)

from logging import getLogger
from .hidtransportbase import HidTool
from .hidtransportbase import HidTransportBase


class CyHidApiTransport(HidTransportBase):
    """Implements all Cython / HIDAPI transport methods"""

    def __init__(self):
        self.logger = getLogger(__name__)
        self.logger.debug("Cython HIDAPI transport")
        super(CyHidApiTransport, self).__init__()
        self.blocking = True
        self.hid_device = None

    def _linux_udev_rule_check(self, device):
        """
        Checks whether there might be a missing udev rule
        On Linux systems, a udev rule is required to grant access to USB devices.  If the udev rule is missing,
        the effect is that the VID and PID are readable, but other device properties are blank, and ths device is
        not able to be opened.  If this is the case, hint to the user to add a udev rule.
        :param device: device to check
        """
        if sys.platform == "linux":
            if device.serial_number == "" and device.manufacturer_string == "" and device.product_string == "":
                self.logger.error('Device not recognised - check that a udev rule exists for this device:\n'
                                  'SUBSYSTEM=="usb",ATTRS{idVendor}=="%04X",ATTRS{idProduct}=="%04X",MODE="0666"',
                                  device.vendor_id, device.product_id)

    def detect_devices(self):
        """
        Detect connected CMSIS-DAP devices, populating an internal list
        :return: number of devices connected
        """""
        self.logger.debug("Detecting Atmel/Microchip CMSIS-DAP compliant devices on USB")
        devices = hid.enumerate()
        for device in devices:
            if device['vendor_id'] == 0x03EB:
                # Python 2.7 does not know how to deal with unicode symbols implicitly
                # This code is here to prevent a crash
                try:
                    for key, value in device.items():
                        if isinstance(value, unicode):
                            try:
                                value.encode('ascii')
                            except UnicodeEncodeError:
                                # Replace the string with an ascii string if the encoding fails
                                device[key] = value.encode('ascii', 'replace')
                except NameError:
                    # Python 3 does not have a "unicode" type
                    pass

                log_str = "Detected {:04X}/{:04X}: '{}' ({}) from {}"
                self.logger.debug(log_str.format(device['vendor_id'],
                                                 device['product_id'],
                                                 device['product_string'],
                                                 device['serial_number'],
                                                 device['manufacturer_string']))

                detected_device = HidTool(device['vendor_id'],
                                          device['product_id'],
                                          device['serial_number'],
                                          device['product_string'],
                                          device['manufacturer_string'])
                self._linux_udev_rule_check(detected_device)

                # Default to 64 until proven otherwise
                detected_device.packet_size = 64
                self.devices.append(detected_device)
        return len(self.devices)

    def hid_connect(self, device):
        """
        Make a HID connection to the debugger

        :param device:
        :return:
        """
        self.logger.debug(
            "Opening 0x%04X/%04X: '%s' (%s)",
            device.vendor_id, device.product_id, device.product_string, device.serial_number)
        hid_device = hid.device()
        try:
            hid_device.open(device.vendor_id, device.product_id, device.serial_number)
        except OSError:
            self._linux_udev_rule_check(device)
            raise
        self.hid_device = hid_device

        # Set blocking by HIDAPI or by Python
        if self.blocking:
            hid_device.set_nonblocking(0)
        else:
            hid_device.set_nonblocking(1)

        return device

    def hid_disconnect(self):
        """
        Disconnect from HID

        :return:
        """
        self.logger.debug("Disconncting HID")
        self.hid_device.close()

    def hid_info(self):
        """
        Retrieve USB descriptor information

        :return:
        """
        self.logger.info("Manufacturer: {:s}".format(
            self.hid_device.get_manufacturer_string()))
        self.logger.info("Product: {:s}".format(
            self.hid_device.get_product_string()))
        self.logger.info("Serial Number: {:s}".format(
            self.hid_device.get_serial_number_string()))

    @staticmethod
    def _hid_pad(data, size):
        # Always send a full frame, plus the bonus-byte
        while len(data) < size:
            data.append(0x00)
        # Put in the bonus byte
        return bytearray([0]) + data

    def hid_transfer(self, data_send):
        """
        Sends HID data and receives response

        :param data_send:
        :return: response
        """
        self.hid_write(data_send)
        return self.hid_read()

    def hid_write(self, data_send):
        """
        Sends HID data

        :param data_send: data to send
        :return: number of bytes sent
        """
        # pad
        data_send = self._hid_pad(data_send, self.device.packet_size)

        # Write
        self.logger.debug("HID::write of {:d} bytes".format(len(data_send)))
        numbytes = self.hid_device.write(data_send)
        self.logger.debug("HID::write sent {:d} bytes".format(numbytes))
        return numbytes

    def hid_read(self):
        """
        Reads HID data

        :return: data read
        """
        self.logger.debug("HID::read")
        if self.blocking:
            response = self.hid_device.read(self.device.packet_size)
        else:
            response = []
            while not response:
                # TODO: Non-blocking mode should have a timeout here.
                response = self.hid_device.read(self.device.packet_size)
        self.logger.debug("HID::read read {:d} bytes".format(len(response)))
        return bytearray(response)
