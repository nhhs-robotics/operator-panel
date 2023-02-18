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

## Turn light on
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
led.value = True

gp = Gamepad(usb_hid.devices)

# Create some buttons. The physical buttons are connected
# to ground on one side and these and these pins on the other.
## button_pins = (board.D2, board.D3, board.D4, board.D5)
button_pins = (board.GP0, board.GP1, board.GP2, board.GP3, board.GP4, board.GP5, board.GP6, board.GP7)

# Map the buttons to button numbers on the Gamepad.
# gamepad_buttons[i] will send that button number when buttons[i]
# is pushed.
gamepad_buttons = (1, 2, 3, 4, 5, 6, 7, 8)

buttons = [digitalio.DigitalInOut(pin) for pin in button_pins]
for button in buttons:
   button.direction = digitalio.Direction.INPUT
   button.pull = digitalio.Pull.UP

toggle_pins = (board.GP8, board.GP9, board.GP10, board.GP11)
toggle_ids = (1, 2, 3, 4)

toggles = [digitalio.DigitalInOut(pin) for pin in toggle_pins]
for toggle in toggles:
   toggle.direction = digitalio.Direction.INPUT
   toggle.pull = digitalio.Pull.UP


# button_pin = board.GP15
# button1 = digitalio.DigitalInOut(button_pin)
# button1.direction = digitalio.Direction.INPUT
# button1.pull = digitalio.Pull.UP
# button2_pin = board.GP14
# button2 = digitalio.DigitalInOut(button2_pin)
# button2.direction = digitalio.Direction.INPUT
# button2.pull = digitalio.Pull.UP

joystick_left_pin = board.GP10
joystick_right_pin = board.GP11
joystick_up_pin = board.GP12
joystick_down_pin = board.GP13

joystick_up = digitalio.DigitalInOut(joystick_up_pin)
joystick_up.direction = digitalio.Direction.INPUT
joystick_up.pull = digitalio.Pull.UP

joystick_down = digitalio.DigitalInOut(joystick_down_pin)
joystick_down.direction = digitalio.Direction.INPUT
joystick_down.pull = digitalio.Pull.UP

joystick_left = digitalio.DigitalInOut(joystick_left_pin)
joystick_left.direction = digitalio.Direction.INPUT
joystick_left.pull = digitalio.Pull.UP

joystick_right = digitalio.DigitalInOut(joystick_right_pin)
joystick_right.direction = digitalio.Direction.INPUT
joystick_right.pull = digitalio.Pull.UP

# Connect an analog two-axis joystick to A4 and A5.
ax = analogio.AnalogIn(board.A0)
ay = analogio.AnalogIn(board.A1)


slider = analogio.AnalogIn(board.A2)


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
    return 0

while True:
    # print("loop")
    print("up: " + str(joystick_up.value))
    print("down: " + str(joystick_down.value))
    print("left: " + str(joystick_left.value))
    print("right: " + str(joystick_right.value))

    direction = direction_map(not joystick_up.value, not joystick_down.value, not joystick_left.value, not joystick_right.value)


    print("direction: " + str(direction))
    gp.move_hat(direction)

    time.sleep(1)


