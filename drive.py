import pybox
from adafruit_servokit import ServoKit
import math
import time

kit = ServoKit(channels=16)

pybox.init()

try:
    while True:
        if abs(pybox.get_r_trigger()) > 0.1 or abs(pybox.get_r_joy_x()) > 0.1 or abs(pybox.get_l_trigger()) > 0.1:
            joystick_x = pybox.get_r_joy_x()
            joystick_y = pybox.get_r_trigger() - pybox.get_l_trigger()
            motorA_speed = 100 * joystick_y + 100 * joystick_x
            motorB_speed = 100 * joystick_y - 100 * joystick_x
            motorA_speed = max(-100, min(100, motorA_speed))/-150
            motorB_speed = max(-100, min(100, motorB_speed))/-150
            kit.continuous_servo[0].throttle = -motorA_speed + 0.3
            kit.continuous_servo[1].throttle = motorB_speed
        else:
            kit.continuous_servo[0].throttle = 0.1
            kit.continuous_servo[1].throttle = 0.1
        time.sleep(0.01)
except KeyboardInterrupt:
    pybox.stop()
