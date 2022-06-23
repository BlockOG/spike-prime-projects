# LEGO type:standard slot:12
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
motors.move_tank(180, "degrees", speed, -speed)
motors.move(22)
hub.motion.yaw_pitch_roll(0)
motors.move_tank(180, "degrees", speed, -speed)
motors.move(45)
hub.motion.yaw_pitch_roll(0)
motors.move_tank(-90, "degrees", speed, -speed)
motors.move(37.5)
hub.motion.yaw_pitch_roll(0)
motors.move_tank(-90, "degrees", speed, -speed)
motors.move(25)
hub.motion.yaw_pitch_roll(0)
motors.move_tank(-180, "degrees", speed, -speed)
motors.move(5)

arm.run_to_position(350)

motors.move(-5)
hub.motion.yaw_pitch_roll(0)
motors.move_tank(360, "degrees", speed, -speed)
motors.move(10)

arm.run_to_position(90)

motors.move(-10)
hub.motion.yaw_pitch_roll(0)
motors.move_tank(-180, "degrees", speed, -speed)
motors.move(-25)
hub.motion.yaw_pitch_roll(0)
motors.move_tank(90, "degrees", speed, -speed)
motors.move(-37.5)
hub.motion.yaw_pitch_roll(0)
motors.move_tank(90, "degrees", speed, -speed)
motors.move(-45)
hub.motion.yaw_pitch_roll(0)
motors.move_tank(-180, "degrees", speed, -speed)
motors.move(-22)
hub.motion.yaw_pitch_roll(0)
motors.move_tank(-180, "degrees", speed, -speed)
motors.move(-20)
hub.motion.yaw_pitch_roll(0)
motors.move_tank(-180, "degrees", speed, -speed)
