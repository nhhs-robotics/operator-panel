# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# You must add a gamepad HID device inside your boot.py file
# in order to use this example.
# See this Learn Guide for details:
# https://learn.adafruit.com/customizing-usb-devices-in-circuitpython/hid-devices#custom-hid-devices-3096614-9

import board
import digitalio
import analogio
import usb_hid
import time

from hid_gamepad import Gamepad

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
led.value = True

print("starting, yo")
print(usb_hid.devices)
gp = Gamepad(usb_hid.devices)

print("gamepad created")

# Create some buttons. The physical buttons are connected
# to ground on one side and these and these pins on the other.
## button_pins = (board.D2, board.D3, board.D4, board.D5)
## button_pins = (board.D2, board.D3, board.D4, board.D5)

# Map the buttons to button numbers on the Gamepad.
# gamepad_buttons[i] will send that button number when buttons[i]
# is pushed.
gamepad_buttons = (1, 2, 8, 15)

#buttons = [digitalio.DigitalInOut(pin) for pin in button_pins]
#for button in buttons:
#    button.direction = digitalio.Direction.INPUT
#    button.pull = digitalio.Pull.UP

button_pin = board.GP15
button1 = digitalio.DigitalInOut(button_pin)
button1.direction = digitalio.Direction.INPUT
button1.pull = digitalio.Pull.UP
button2_pin = board.GP14
button2 = digitalio.DigitalInOut(button2_pin)
button2.direction = digitalio.Direction.INPUT
button2.pull = digitalio.Pull.UP

joystick_up_pin = board.GP10
joystick_down_pin = board.GP11
joystick_right_pin = board.GP12
joystick_left_pin = board.GP13

joystick_up = digitalio.DigitalInOut(joystick_up_pin)
joystick_up.direction = digitalio.Direction.INPUT
joystick_up.pull = digitalio.Pull.DOWN

joystick_down = digitalio.DigitalInOut(joystick_down_pin)
joystick_down.direction = digitalio.Direction.INPUT
joystick_down.pull = digitalio.Pull.UP


# Connect an analog two-axis joystick to A4 and A5.
ax = analogio.AnalogIn(board.A0)
slider = analogio.AnalogIn(board.A2)
ay = analogio.AnalogIn(board.A1)


# ax = digitalio.DigitalInOut(board.GP10)
# ax.direction = digitalio.Direction.INPUT
# ay = digitalio.DigitalInOut(board.GP11)
# ay.direction = digitalio.Direction.INPUT

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


while True:
    # print("loop")

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
    gp.set_sliderX(85)
    time.sleep(1)
    print("Set sliderY")
    gp.set_sliderY(127) ## TODO: Getting bigger than 127
    time.sleep(1)

    print("Release button2")
    gp.release_buttons(2)
    time.sleep(1)
    print("Set joystick North")
    gp.set_analog_joystick(Gamepad.JOYSTICK_NORTH)
    time.sleep(1)
    print("Set joystick NW")
    gp.set_analog_joystick(Gamepad.JOYSTICK_NW) ## Setting this causes overflow
    time.sleep(1)
    print("Set joystick South")
    gp.set_analog_joystick(Gamepad.JOYSTICK_SOUTH)
    time.sleep(1)

    print("Set joystick Home")
    gp.set_analog_joystick(Gamepad.JOYSTICK_HOME)

    time.sleep(1)

