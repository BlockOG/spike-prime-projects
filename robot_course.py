# LEGO type:standard slot:7
from spike import MotorPair, LightMatrix
import hub

motors = MotorPair("C", "D")


def rotate_degrees_pivot(degrees, speed=10):
    hub.motion.yaw_pitch_roll(0)
    if degrees < 0:
        motors.move_tank(degrees * 2, "degrees", speed, 0)
    else:
        motors.move_tank(degrees * 2, "degrees", 0, speed)


def rotate_degrees_center(degrees, speed=10):
    hub.motion.yaw_pitch_roll(0)
    motors.move_tank(degrees * 2, "degrees", speed, -speed)


motors.move(25)

rotate_degrees_center(90)

motors.move(63)

rotate_degrees_pivot(-90)

motors.move(40)
