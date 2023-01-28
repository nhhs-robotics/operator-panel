# Prototype Code for Draft 2

The goal of this code is to get the HID descriptor correct for our operator panel: 

* 8-10 (figure out the right amount) buttons for the buttons and switches
* Analog inputs from the sliders
* POV input from the digital joystick



* Need to download the Adafruit hid library and copy into the lib/ dir on the Pico


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
    

