# Prototype Code for Draft 2

The goal of this code is to get the HID descriptor correct for our operator panel: 

* 8-10 (figure out the right amount) buttons for the buttons and switches
* Analog inputs from the sliders
* POV input from the digital joystick



* Need to download the Adafruit hid library and copy into the lib/ dir on the Pico

## Notes 

The way a USB HID device works is that when the device is plugged into the USB host (the computer), it starts by sending a **USB HID Descriptor** that specifies what kind of device it is and the format of the data that will be sent. Then, every so often, the device sends a **USB HID Report** that states the current status of the device. 

So, the ***descriptor*** says what data is in which bit, and the ***report*** sends the actual bits. 

Our descriptor contains 3 components: 
* Some buttons (right now, 16)
* Some axes (e.g., an analog joystick)
* A "hat switch" (e.g. the digital joystick)

To describe the buttons: 

```
    0x05, 0x09,  #   Usage Page (Button)
    0x19, 0x01,  #   Usage Minimum (Button 1)
    0x29, 0x10,  #   Usage Maximum (Button 16)
    0x15, 0x00,  #   Logical Minimum (0)
    0x25, 0x01,  #   Logical Maximum (1)
    0x75, 0x01,  #   Report Size (1)
    0x95, 0x10,  #   Report Count (16)
    0x81, 0x02,  #   Input (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
```

This says: 

* `Usage Page (Button)`: We're defining a *usage page* that describes a button input
* `Usage Minimum`, `Usage Maximum`: We have 16 buttons
* `Logical Minimum`, `Logical Maximum`: Each button will be reported with a value of 0 or 1
* `Report Size`: Each button will use 1 bit in the report
* `Report Count`: There will 16 "copies of the report", one for each button
* `Input`: I think this basically indicates the "end of the report". 

To describe the analog joystick: 

```
    0x05, 0x01,  #   Usage Page (Generic Desktop Ctrls)
    0x15, 0x81,  #   Logical Minimum (-127)
    0x25, 0x7F,  #   Logical Maximum (127)
    0x09, 0x30,  #   Usage (X)
    0x09, 0x31,  #   Usage (Y)
    0x09, 0x32,  #   Usage (Z)
    0x09, 0x35,  #   Usage (Rz)
    0x75, 0x08,  #   Report Size (8)
    0x95, 0x04,  #   Report Count (4)
    0x81, 0x02,  #   Input (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)

```

* `Usage Page`: Now we're starting to describe a desktop control 
* The values of the values in this part of the report will be -127 to 127
* The 4 `Usage` lines indicate that we'll have 4 values reported that are described by the next few lines
* Each of those values will be 8 bits/1 byte
* There will be 4 of those values
* `Input` indicates the end of this section

To describe the digital joystick: 

```
    0x09, 0x39,  #   USAGE (Hat switch)
    0x15, 0x00,  #   LOGICAL_MINIMUM(0)
    0x25, 0x03,  #   LOGICAL_MAXIMUM(3)
    0x35, 0x00,  #   PHYSICAL_MINIMUM(0)
    0x46, 0x0E, 0x01, # PHYSICAL_MAXIMUM(270)
    0x65, 0x14,  #   UNIT (Eng Rot:Angular Pos)
    0x75, 0x04,  #   REPORT_SIZE(4)
    0x95, 0x01,  #   REPORT_COUNT(1)
    0x81, 0x02,  #   Input (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
```

* Now we're describing input from a "hat switch"-- a button that has a "neutral" position, but can be moved in a number of directions
* This hat switch has 4 values


* Need to specify the USB HID Descriptor in `boot.py`
    * The descriptor describes the *report* that is sent via the `hid_gamepad.py` file.


# Resources

* [USB Joystick](https://helmpcb.com/electronics/usb-joystick)
    * Shows the HID descriptor for a POV joystick
* [Modifying the USB HID Joystick Descriptor](https://helmpcb.com/electronics/modifying-the-joystick-hid-descriptor)
    * More details about how to modify the descriptor
* [Tutorial for USB HID Descriptors](https://eleccelerator.com/tutorial-about-usb-hid-report-descriptors/)
    * Provides an overview of how HID descriptors work
* [USB Descriptor Parser](http://eleccelerator.com/usbdescreqparser/)
    * Might be helpful for debugging/fixing the report/descriptor
* [Understanding the Xbox 360 Wired Controller’s USB Data](https://www.partsnotincluded.com/understanding-the-xbox-360-wired-controllers-usb-data/)
    * Might be helpful for reference/context/example


