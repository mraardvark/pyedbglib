"""
Gathering of all known Atmel/Microchip CMSIS-DAP debuggers and default EP sizes
"""
import logging

# List of known useful HID/CMSIS-DAP tools
# 3G tools:
USB_TOOL_DEVICE_PRODUCT_ID_JTAGICE3 = 0x2140
USB_TOOL_DEVICE_PRODUCT_ID_ATMELICE = 0x2141
USB_TOOL_DEVICE_PRODUCT_ID_POWERDEBUGGER = 0x2144
USB_TOOL_DEVICE_PRODUCT_ID_EDBG_A = 0x2111
USB_TOOL_DEVICE_PRODUCT_ID_ZERO = 0x2157
USB_TOOL_DEVICE_PRODUCT_ID_MASS_STORAGE = 0x2169
USB_TOOL_DEVICE_PRODUCT_ID_PUBLIC_EDBG_C = 0x216A
USB_TOOL_DEVICE_PRODUCT_ID_KRAKEN = 0x2170

# 4G tools:
USB_TOOL_DEVICE_PRODUCT_ID_MEDBG = 0x2145

# 5G tools:
USB_TOOL_DEVICE_PRODUCT_ID_NEDBG_HID = 0x2172
USB_TOOL_DEVICE_PRODUCT_ID_NEDBG_HID_CDC = 0x216F
USB_TOOL_DEVICE_PRODUCT_ID_NEDBG_HID_MSD_CDC = 0x2173
USB_TOOL_DEVICE_PRODUCT_ID_NEDBG_HID_DGI_CDC = 0x2174
USB_TOOL_DEVICE_PRODUCT_ID_NEDBG_HID_MSD_DGI_CDC = 0x2175

USB_TOOL_DEVICE_PRODUCT_ID_PICKIT4_HID = 0x2176
USB_TOOL_DEVICE_PRODUCT_ID_PICKIT4_HID_CDC = 0x2177


def get_default_report_size(pid):
    """
    Retrieve default EP report size based on known PIDs
    :param pid: product ID
    :return: packet size
    """
    logger = logging.getLogger(__name__)
    logger.addHandler(logging.NullHandler())
    hid_tools = [
        # 3G
        {'pid': USB_TOOL_DEVICE_PRODUCT_ID_JTAGICE3, 'default_report_size': 512},
        {'pid': USB_TOOL_DEVICE_PRODUCT_ID_ATMELICE, 'default_report_size': 512},
        {'pid': USB_TOOL_DEVICE_PRODUCT_ID_POWERDEBUGGER, 'default_report_size': 512},
        {'pid': USB_TOOL_DEVICE_PRODUCT_ID_EDBG_A, 'default_report_size': 512},
        # 4G
        {'pid': USB_TOOL_DEVICE_PRODUCT_ID_MEDBG, 'default_report_size': 64},
        # 5G
        {'pid': USB_TOOL_DEVICE_PRODUCT_ID_NEDBG_HID_MSD_DGI_CDC, 'default_report_size': 64},
        {'pid': USB_TOOL_DEVICE_PRODUCT_ID_PICKIT4_HID, 'default_report_size': 64},
        {'pid': USB_TOOL_DEVICE_PRODUCT_ID_PICKIT4_HID_CDC, 'default_report_size': 64}]

    logger.debug("Looking up report size for pid 0x{:04X}".format(pid))
    for tool in hid_tools:
        if tool['pid'] == pid:
            logger.debug("Default report size is {:d}".format(tool['default_report_size']))
            return tool['default_report_size']
    logger.debug("PID not found! Reverting to 64b.")
    return 64
