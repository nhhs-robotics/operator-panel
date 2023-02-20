
import board
import digitalio
import analogio
import usb_hid
import time

from hid_gamepad import Gamepad
from test_gamepad import run_test

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
led.value = True

print("starting, yo")
print(usb_hid.devices)
gp = Gamepad(usb_hid.devices)

print("gamepad created")


while True:
    run_test(gp)
    
    # # print("loop")

    # gp.press_buttons(2)
    # print("Turn toggle1 on")
    # gp.toggle_on(1)
    # time.sleep(1)
    # print("Turn toggle2 on")
    # gp.toggle_on(2)
    # time.sleep(1)
    # print("Turn toggle3 on")
    # gp.toggle_on(3)
    # time.sleep(1)
    # print("Turn toggle4 on")
    # gp.toggle_on(4)
    # time.sleep(1)
    # gp.toggle_off(1,2,3,4)

    # print("Set sliderX")
    # gp.set_sliderX(85)
    # time.sleep(1)
    # print("Set sliderY")
    # gp.set_sliderY(127) ## TODO: Getting bigger than 127
    # time.sleep(1)

    # print("Release button2")
    # gp.release_buttons(2)
    # time.sleep(1)
    # print("Set joystick North")
    # gp.set_analog_joystick(Gamepad.JOYSTICK_NORTH)
    # time.sleep(1)
    # print("Set joystick NW")
    # gp.set_analog_joystick(Gamepad.JOYSTICK_NW) ## Setting this causes overflow
    # time.sleep(1)
    # print("Set joystick South")
    # gp.set_analog_joystick(Gamepad.JOYSTICK_SOUTH)
    # time.sleep(1)

    # print("Set joystick Home")
    # gp.set_analog_joystick(Gamepad.JOYSTICK_HOME)

    time.sleep(1)

