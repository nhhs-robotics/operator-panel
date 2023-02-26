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
from rainbowio import colorwheel
import neopixel
from neopixel_helpers import rainbow_cycle, neopix_test, neopix_twinkle_test


from hid_gamepad import Gamepad

gp = Gamepad(usb_hid.devices)

# Create some buttons. The physical buttons are connected
# to ground on one side and these and these pins on the other.
button_pins = (board.GP0, board.GP1, board.GP2, board.GP3, board.GP4, board.GP5, board.GP6, board.GP7 )

# Map the buttons to button numbers on the Gamepad.
# gamepad_buttons[i] will send that button number when buttons[i]
# is pushed.
gamepad_buttons = (1, 2, 3, 4, 5, 6, 7, 8)

buttons = [digitalio.DigitalInOut(pin) for pin in button_pins]
for button in buttons:
   button.direction = digitalio.Direction.INPUT
   button.pull = digitalio.Pull.UP

# Create some toggles. The physical toggles are connected
# to ground on one side and these and these pins on the other.
toggle_pins = (board.GP10, board.GP11, board.GP12, board.GP13)

# Map the toggles to toggle numbers on the Gamepad.
# gamepad_toggles[i] will send that toggle number when toggles[i]
# is pushed.
gamepad_toggles = (1, 2, 3, 4)

toggles = [digitalio.DigitalInOut(pin) for pin in toggle_pins]
for toggle in toggles:
   toggle.direction = digitalio.Direction.INPUT
   toggle.pull = digitalio.Pull.UP

# Create the Joystick hat switches
joystick_down_pin = board.GP18
joystick_up_pin = board.GP19
joystick_right_pin = board.GP20
joystick_left_pin = board.GP21

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

# Set up the analog sliders
sliderX = analogio.AnalogIn(board.A0)
sliderY = analogio.AnalogIn(board.A1)

pixel_pin = board.A2

num_pixels = 30

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.3, auto_write=False)


# Equivalent of Arduino's map() function.
def range_map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min


## Takes in the value of the hat switches (which ones are on/off)
## and returns a Gamepad JOYSTICK direction
## TODO: we can totally do this more efficiently, but eh
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


def send_buttons():
    # Buttons are grounded when pressed (.value = False).
    for i, button in enumerate(buttons):
        gamepad_button_num = gamepad_buttons[i]
        if button.value:
            gp.release_buttons(gamepad_button_num)
            print(" release", gamepad_button_num, end="")
        else:
            gp.press_buttons(gamepad_button_num)
            print(" press", gamepad_button_num, end="")

def send_toggles():
    # Toggles are grounded when pressed (.value = False).
    for i, toggle in enumerate(toggles):
        gamepad_toggle_num = gamepad_toggles[i]
        if toggle.value:
            gp.toggle_off(gamepad_toggle_num) ## TODO: Make sure this is the right direction
            print(" toggleOff: ", gamepad_toggle_num, end="")
        else:
            gp.toggle_on(gamepad_toggle_num)
            print(" toggleOn: ", gamepad_toggle_num, end="")

def send_sliders():
    # Convert range[0, 65535] to 0 to 255
    # gp.move_joysticks(
    #     x=range_map(ax.value, 0, 65535, -127, 127),
    #     y=range_map(ay.value, 0, 65535, -127, 127),
    # )
    gp.set_sliderX(range_map(sliderX.value, 0, 65535, 0, 255))
    gp.set_sliderY(range_map(sliderY.value, 0, 65535, 0, 255))

def send_joystick():
    print("Up: " + str(not joystick_up.value))
    print(not joystick_down.value)
    print(not joystick_left.value)
    print(not joystick_right.value)
    gp.set_digital_joystick(direction_map(not joystick_up.value,
                                          not joystick_down.value,
                                          not joystick_left.value,
                                          not joystick_right.value))

# while True:
#     # print("loop")
#     send_buttons()
#     send_toggles()
#     send_sliders()
#     send_joystick()

#     time.sleep(1)

def send_widget_states():
    send_buttons()
    send_toggles()
    send_sliders()
    send_joystick()
    #rainbow_cycle(pixels,0)
    neopix_twinkle_test(pixels,0.1)
