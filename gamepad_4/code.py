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


while True:
    # print("loop")
    # Buttons are grounded when pressed (.value = False).
#    for i, button in enumerate(buttons):
#        gamepad_button_num = gamepad_buttons[i]
#        if button.value:
#            gp.release_buttons(gamepad_button_num)
#            print(" release", gamepad_button_num, end="")
#        else:
#            gp.press_buttons(gamepad_button_num)
#            print(" press", gamepad_button_num, end="")
    if button1.value:
        gp.release_buttons(1)
        # print("release 1")
    else:
        gp.press_buttons(1)
        print("press 1")
    if button2.value:
        gp.release_buttons(2)
    else:
        gp.press_buttons(2)
        print("press 2")


    # Convert range[0, 65535] to -127 to 127
    gp.move_joysticks(
        x=range_map(ax.value, 0, 65535, -127, 127),
        y=range_map(ay.value, 0, 65535, -127, 127),
        z=range_map(slider.value, 0, 65535, -127, 127),
        r_z=(joystick_down.value),
    )
    #print(" x", ax.value, "y", ay.value)
    # print((ax.value, ay.value,slider.value))
    # print(joystick_up.value)
    time.sleep(0.5)

