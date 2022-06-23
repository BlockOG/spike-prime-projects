# LEGO type:standard slot:5
from spike import Motor, MotorPair
import hub

motors = MotorPair("C", "D")
arm = Motor("E")

speed = 50

motors.set_default_speed(speed)
arm.set_default_speed(speed)

arm.run_to_position(90)
motors.move(20)
hub.motion.yaw_pitch_roll(0)
motors.move_tank(-180, "degrees", speed, -speed)
motors.move(20)
hub.motion.yaw_pitch_roll(0)
motors.move_tank(-180, "degrees", speed, -speed)
motors.move(63)
arm.run_to_position(350)
hub.motion.yaw_pitch_roll(0)
motors.move_tank(360, "degrees", speed, -speed)
motors.move(85)
arm.run_to_position(90)
motors.move(-23)
hub.motion.yaw_pitch_roll(0)
motors.move_tank(-180, "degrees", speed, -speed)
motors.move(-20)
hub.motion.yaw_pitch_roll(0)
motors.move_tank(180, "degrees", speed, -speed)
motors.move(-20)
