# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# You must add a gamepad HID device inside your boot.py file
# in order to use this example.
# See this Learn Guide for details:
# https://learn.adafruit.com/customizing-usb-devices-in-circuitpython/hid-devices#custom-hid-devices-3096614-9


import usb_hid
import time

from hid_gamepad import Gamepad


print("starting, yo")
print(usb_hid.devices)
gp = Gamepad(usb_hid.devices)

print("gamepad created")

# Equivalent of Arduino's map() function.
def range_map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min


def direction_map(up, down, left, right):
    if up:
        if left:
            return Gamepad.JOYSTICK_NW
        if right:
            return Gamepad.JOYSTICK_NE
        return Gamepad.JOYSTICK_NORTH
    if down:
        if left:
            return Gamepad.JOYSTICK_SW
        if right:
            return Gamepad.JOYSTICK_SE
        return Gamepad.JOYSTICK_SOUTH
    if left:
        return Gamepad.JOYSTICK_WEST
    if right:
        return Gamepad.JOYSTICK_EAST
    return Gamepad.JOYSTICK_HOME

def run_test(gp): 
    gp.press_buttons(2)
    print("Turn toggle1 on")
    gp.toggle_on(1)
    time.sleep(1)
    print("Turn toggle2 on")
    gp.toggle_on(2)
    time.sleep(1)
    print("Turn toggle3 on")
    gp.toggle_on(3)
    time.sleep(1)
    print("Turn toggle4 on")
    gp.toggle_on(4)
    time.sleep(1)
    gp.toggle_off(1,2,3,4)

    print("Set sliderX")
    gp.set_sliderX(0)
    time.sleep(1)
    gp.set_sliderX(255)
    print("Set sliderY")
    gp.set_sliderY(0) ## TODO: Getting bigger than 127
    time.sleep(1)
    gp.set_sliderY(255)

    print("Release button2")
    gp.release_buttons(2)
    time.sleep(1)
    print("Set joystick North")
    gp.set_analog_joystick(Gamepad.JOYSTICK_NORTH)
    time.sleep(1)
    print("Set joystick NW")
    gp.set_analog_joystick(Gamepad.JOYSTICK_NW) 
    time.sleep(1)
    print("Set joystick South")
    gp.set_analog_joystick(Gamepad.JOYSTICK_SOUTH)
    time.sleep(1)

    print("Set joystick Home")
    gp.set_analog_joystick(Gamepad.JOYSTICK_HOME)

    print("Toggle all on and then test the hat")
    gp.toggle_on(1,2,3,4)
    print("Set joystick North")
    gp.set_analog_joystick(Gamepad.JOYSTICK_NORTH)
    time.sleep(1)
    print("Set joystick NW")
    gp.set_analog_joystick(Gamepad.JOYSTICK_NW) 
    time.sleep(1)
    print("Set joystick South")
    gp.set_analog_joystick(Gamepad.JOYSTICK_SOUTH)
    time.sleep(1)

    print("Set joystick Home")
    gp.set_analog_joystick(Gamepad.JOYSTICK_HOME)

    print("Done with test! =============")
