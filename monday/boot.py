import usb_hid


## HID Usage Tables: 1.3.0
## Descriptor size: 62 (bytes)
## +----------+-------+------------------+
## | ReportId | Kind  | ReportSizeInBits |
## +----------+-------+------------------+
## |        1 | Input |               32 |
## +----------+-------+------------------+

# This is only one example of a gamepad descriptor, and may not suit your needs.
GAMEPAD_REPORT_DESCRIPTOR = bytes((
    0x05, 0x01,          ## UsagePage(Generic Desktop[1])
    0x09, 0x05,          ## UsageId(Gamepad[5])
    0xA1, 0x01,          ## Collection(Application)
    0x85, 0x04,          ##     ReportId(1)
    0x09, 0x01,          ##     UsageId(Pointer[1])
    0xA1, 0x00,          ##     Collection(Physical)
    0x09, 0x30,          ##         UsageId(X[48])
    0x09, 0x31,          ##         UsageId(Y[49])
    0x15, 0x00,          ##         LogicalMinimum(0)
    0x26, 0xFF, 0x00,    ##         LogicalMaximum(255)
    0x95, 0x02,          ##         ReportCount(2)
    0x75, 0x08,          ##         ReportSize(8)
    0x81, 0x02,          ##         Input(Data, Variable, Absolute, NoWrap, Linear, PreferredState, NoNullPosition, BitField)
    0xC0,                ##     EndCollection()
    0x05, 0x09,          ##     UsagePage(Button[9])
    0x19, 0x01,          ##     UsageIdMin(Button 1[1])
    0x29, 0x0C,          ##     UsageIdMax(Button 12[12])
    0x25, 0x01,          ##     LogicalMaximum(1)
    0x95, 0x0C,          ##     ReportCount(12)
    0x75, 0x01,          ##     ReportSize(1)
    0x81, 0x02,          ##     Input(Data, Variable, Absolute, NoWrap, Linear, PreferredState, NoNullPosition, BitField)
    0x05, 0x01,          ##     UsagePage(Generic Desktop[1])
    0x09, 0x39,          ##     UsageId(Hat Switch[57])
    0x46, 0x3B, 0x01,    ##     PhysicalMaximum(315)
    0x65, 0x14,          ##     Unit('degrees', EnglishRotation, Degrees:1)
    0x15, 0x01,          ##     LogicalMinimum(1)
    0x25, 0x08,          ##     LogicalMaximum(8)
    0x95, 0x01,          ##     ReportCount(1)
    0x75, 0x04,          ##     ReportSize(4)
    0x81, 0x42,          ##     Input(Data, Variable, Absolute, NoWrap, Linear, PreferredState, NullState, BitField)
    0xC0,                ## EndCollection()
))

gamepad = usb_hid.Device(
    report_descriptor=GAMEPAD_REPORT_DESCRIPTOR,
    usage_page=0x01,           # Generic Desktop Control
    usage=0x05,                # Gamepad
    report_ids=(4,),           # Descriptor uses report ID 4.
    in_report_lengths=(4,),    # This gamepad sends 4 bytes in its report.
    out_report_lengths=(0,),   # It does not receive any reports.
)

usb_hid.enable(
    (usb_hid.Device.KEYBOARD,
     usb_hid.Device.MOUSE,
     gamepad)
)
