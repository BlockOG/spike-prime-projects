# LEGO type:standard slot:2
from spike import Motor, MotorPair, PrimeHub
from spike.control import wait_for_seconds
import hub

motors = MotorPair("C", "D")
arm = Motor("E")

speed = 50

motors.set_default_speed(speed)
arm.set_default_speed(speed)

hub.display.show(
    [
        hub.Image("00000:00000:00000:00000:00000"),
        hub.Image("00009:00009:00009:00009:00009"),
        hub.Image("00099:00090:00099:00090:00099"),
        hub.Image("00999:00900:00999:00900:00999"),
        hub.Image("09999:09000:09999:09000:09999"),
        hub.Image("99999:90009:99990:90009:99999"),
    ],
    delay=100,
    clear=False,
    wait=False,
    loop=False,
    fade=0,
)

PrimeHub().right_button.wait_until_pressed()
wait_for_seconds(0.5)

arm.run_to_position(90)
motors.move(15)
arm.run_to_position(350)
motors.move(-15)

hub.display.show(
    [
        hub.Image("99990:00090:99900:00090:99990"),
        hub.Image("99909:00909:99009:00909:99909"),
        hub.Image("99099:09090:90090:09090:99099"),
        hub.Image("90999:90900:00900:90900:90999"),
        hub.Image("09999:09000:09000:09000:09999"),
        hub.Image("99999:90000:90000:90000:99999"),
    ],
    delay=100,
    clear=False,
    wait=False,
    loop=False,
    fade=0,
)

PrimeHub().right_button.wait_until_pressed()
wait_for_seconds(0.5)

motors.move(20)
hub.motion.yaw_pitch_roll(0)
motors.move_tank(180, "degrees", speed, -speed)
motors.move(17)
hub.motion.yaw_pitch_roll(0)
motors.move_tank(180, "degrees", speed, -speed)
motors.move(12)

arm.run_to_position(90)

motors.move(-12)
hub.motion.yaw_pitch_roll(0)
motors.move_tank(-180, "degrees", speed, -speed)
motors.move(-17)
hub.motion.yaw_pitch_roll(0)
motors.move_tank(-180, "degrees", speed, -speed)
motors.move(-20)

hub.display.show(
    [
        hub.Image("99999:90000:90000:90000:99999"),
        hub.Image("99990:00000:00000:00000:99990"),
        hub.Image("99900:00000:00000:00000:99900"),
        hub.Image("99000:00000:00000:00000:99000"),
        hub.Image("90000:00000:00000:00000:90000"),
        hub.Image("00000:00000:00000:00000:00000"),
    ],
    delay=100,
    clear=False,
    wait=True,
    loop=False,
    fade=0,
)
