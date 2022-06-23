# LEGO type:standard slot:8
from spike import Motor, MotorPair, PrimeHub
from spike.control import wait_for_seconds
import hub

motors = MotorPair("C", "D")
arm = Motor("E")

speed = 50

motors.set_default_speed(speed)
arm.set_default_speed(speed)

arm.run_to_position(90)

motors.move(25)
hub.motion.yaw_pitch_roll(0)
motors.move_tank(180, "degrees", speed, -speed)
motors.move(70)
hub.motion.yaw_pitch_roll(0)
motors.move_tank(-180, "degrees", speed, -speed)
motors.move(25)
hub.motion.yaw_pitch_roll(0)
motors.move_tank(180, "degrees", speed, -speed)
motors.move(20)
hub.motion.yaw_pitch_roll(0)
motors.move_tank(180, "degrees", speed, -speed)
motors.move(25)

arm.run_to_position(350)

motors.move(-25)
hub.motion.yaw_pitch_roll(0)
motors.move_tank(-180, "degrees", speed, -speed)
motors.move(-20)
hub.motion.yaw_pitch_roll(0)
motors.move_tank(-180, "degrees", speed, -speed)
motors.move(-25)
hub.motion.yaw_pitch_roll(0)
motors.move_tank(180, "degrees", speed, -speed)
motors.move(-70)
hub.motion.yaw_pitch_roll(0)
motors.move_tank(-180, "degrees", speed, -speed)
motors.move(-25)

PrimeHub().right_button.wait_until_pressed()
wait_for_seconds(0.5)

motors.move(20)
hub.motion.yaw_pitch_roll(0)
motors.move_tank(180, "degrees", speed, -speed)
motors.move(22.5)
hub.motion.yaw_pitch_roll(0)
motors.move_tank(180, "degrees", speed, -speed)
motors.move(55)
hub.motion.yaw_pitch_roll(0)
motors.move_tank(20, "degrees", speed, -speed)
motors.move(7)

arm.run_to_position(90)

motors.move(-7)
hub.motion.yaw_pitch_roll(0)
motors.move_tank(-20, "degrees", speed, -speed)
motors.move(-55)
hub.motion.yaw_pitch_roll(0)
motors.move_tank(-180, "degrees", speed, -speed)
motors.move(-22.5)
hub.motion.yaw_pitch_roll(0)
motors.move_tank(-180, "degrees", speed, -speed)
motors.move(-20)
