
import board
import digitalio
import analogio
import usb_hid
import time

from hid_gamepad import Gamepad
from test_gamepad import run_test, test_toggles

# import robot_control_panel
from robot_control_panel import send_widget_states

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
led.value = True

print("starting, yo")
# print(usb_hid.devices)
gp = Gamepad(usb_hid.devices)

# print("gamepad created")


while True:
    run_test(gp)
    test_toggles(gp)
    # send_widget_states()

    time.sleep(1)

