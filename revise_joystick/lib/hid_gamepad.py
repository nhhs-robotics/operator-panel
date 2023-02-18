# Write your code here :-)
# SPDX-FileCopyrightText: 2018 Dan Halbert for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`Gamepad`
====================================================

* Author(s): Dan Halbert
"""

import struct
import time
import sys

from adafruit_hid import find_device


class Gamepad:
    """Emulate a generic gamepad controller with 16 buttons,
    numbered 1-16, and two joysticks, one controlling
    ``x` and ``y`` values, and the other controlling ``z`` and
    ``r_z`` (z rotation or ``Rz``) values.

    The joystick values could be interpreted
    differently by the receiving program: those are just the names used here.
    The joystick values are in the range -127 to 127.

    Generic Gamepad with:
    2 sliders
    8 buttons
    4 toggles (buttons)
    1 joystick with hatswitch


    """

    JOYSTICK_NORTH = 0
    JOYSTICK_NE = 1
    JOYSTICK_EAST = 2
    JOYSTICK_SE = 3
    JOYSTICK_SOUTH = 4
    JOYSTICK_SW = 5
    JOYSTICK_WEST = 6
    JOYSTICK_NW = 7

    def __init__(self, devices):
        """Create a Gamepad object that will send USB gamepad HID reports.

        Devices can be a list of devices that includes a gamepad device or a gamepad device
        itself. A device is any object that implements ``send_report()``, ``usage_page`` and
        ``usage``.
        """
        self._gamepad_device = find_device(devices, usage_page=0x1, usage=0x05)

        # Reuse this bytearray to send mouse reports.
        # Typically controllers start numbering buttons at 1 rather than 0.
        # report[0] Slider X
        # report[1] Slider Y
        # report[2,3] buttons 1-8 (LSB is button 1), toggles 1-4, hatswitch
        self._report = bytearray(4)

        # Remember the last report as well, so we can avoid sending
        # duplicate reports.
        self._last_report = bytearray(4)

        # Store settings separately before putting into report. Saves code
        # especially for buttons.
        self._buttons_state = 0
        self._slider_x = 0 ## Val: 0-256 (HID descriptor needs to be updated)
        self._slider_y = 0 ## Val: 0-256 (HID descriptor needs to be updated)
        self._toggles_state = 0
        self._hat = 0   ## Val 0-7, where 0 is 0deg, 7 is 315 deg

        # Send an initial report to test if HID device is ready.
        # If not, wait a bit and try once more.
        try:
            self.reset_all()
        except OSError:
            time.sleep(1)
            self.reset_all()

    def press_buttons(self, *buttons):
        """Press and hold the given buttons."""
        for button in buttons:
            self._buttons_state |= 1 << self._validate_button_number(button) - 1
        self._send()

    def release_buttons(self, *buttons):
        """Release the given buttons."""
        for button in buttons:
            self._buttons_state &= ~(1 << self._validate_button_number(button) - 1)
        self._send()

    def release_all_buttons(self):
        """Release all the buttons."""
        self._buttons_state = 0
        self._send()

    def click_buttons(self, *buttons):
        """Press and release the given buttons."""
        self.press_buttons(*buttons)
        self.release_buttons(*buttons)

    def toggle_on(self, *toggles):
        """Turn toggle switch on"""
        for toggle in toggles:
            self._toggles_state |= 1 << self._validate_toggle_number(toggle) - 1
        self._send()

    def set_sliderX(self, val):
        self.move_joysticks(x=val)

    def set_sliderY(self, val):
        self.move_joysticks(y=val)

    def move_joysticks(self, x=None, y=None, z=None, r_z=None):
        """Set and send the given (analog) joystick values.
        The joysticks will remain set with the given values until changed

        One joystick provides ``x`` and ``y`` values,
        and the other provides ``z`` and ``r_z`` (z rotation).
        Any values left as ``None`` will not be changed.

        All values must be in the range -127 to 127 inclusive.

        Examples::

            # Change x and y values only.
            gp.move_joysticks(x=100, y=-50)

            # Reset all joystick values to center position.
            gp.move_joysticks(0, 0, 0, 0)
        """
        if x is not None:
            self._joy_x = self._validate_joystick_value(x)
        if y is not None:
            self._joy_y = self._validate_joystick_value(y)
        if z is not None:
            self._joy_z = self._validate_joystick_value(z)
        if r_z is not None:
            self._joy_r_z = self._validate_joystick_value(r_z)
        self._send()


    ## Helper method for backwards compat
    def set_analog_joystick(self, dir):
        self.move_hat(dir)

    def move_hat(self, dir):
        self._hat = self._validate_hat_value(dir)
        self._send()


    def reset_all(self):
        """Release all buttons and set joysticks to zero."""
        self._buttons_state = 0
        self._joy_x = 0
        self._joy_y = 0
        self._joy_z = 0
        self._joy_r_z = 0
        self._hat = 0
        self._send(always=True)

    def _pack_toggles_and_hat(self):
        ## TODO: Might need to reverse these
        packed_val = 0
        ## packed_val |= self._toggles_state << 4 ## Toggles are already packed!
        packed_val |= self._hat << 4
        return packed_val

    def _debug_vals(self, packed_bits):
        print("SliderX: " + str(self._slider_x))
        print("SliderY: " + str(self._slider_y))
        print("Buttons: " + str(self._buttons_state))
        print("Toggles: " + str(self._toggles_state))
        print("Hat: " + str(self._hat))
        print("Packed Hat/Toggle: " + str(packed_bits))

    def _send(self, always=False):
        """Send a report with all the existing settings.
        If ``always`` is ``False`` (the default), send only if there have been changes.
        """
        packed_toggles_and_hat = self._pack_toggles_and_hat()

        self._debug_vals(packed_toggles_and_hat)

        struct.pack_into(
            "<bbbb",  ## Little-endian, H: unsigned short (2 bytes), b: signed char (1 byte)
            self._report, ## Pack into the _report var
            0, ## Offset = 0
            self._joy_x, ## Slider X
            self._joy_y, ## Slider Y
            self._buttons_state, ## Write the button state, little-endian
            packed_toggles_and_hat,
        )
        #print(self._report)
        #print("sending report")


        if always or self._last_report != self._report:
            print(self._gamepad_device)
            self._gamepad_device.send_report(self._report)
            # Remember what we sent, without allocating new storage.
            self._last_report[:] = self._report

    @staticmethod
    def _validate_button_number(button):
        if not 1 <= button <= 8:
            raise ValueError("Button number must in range 1 to 8")
        return button

    @staticmethod
    def _validate_toggle_number(value):
        if not 1 <= value <= 4:
            raise ValueError("Toggle value must be in range 1 to 4")
        return value + 8

    @staticmethod
    def _validate_joystick_value(value):
        if not -127 <= value <= 127:
            raise ValueError("Joystick value must be in range -127 to 127")
        return value

    @staticmethod
    def _validate_slider_value(value):
        if not 0 <= value <= 256: ## TODO: Update HID Descriptor
            raise ValueError("Slider value must be in range 0 to 256")
        return value

    @staticmethod
    def _validate_hat_value(value):
        if not 0 <= value <= 7:
            raise ValueError("Joystick value must be in range 0 to 7")
        return value

