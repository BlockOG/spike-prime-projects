# LEGO type:standard slot:17
from spike import Motor, ColorSensor
from spike.control import wait_for_seconds

base = Motor("A")
arm = Motor("B")
claws = Motor("C")
sensor = ColorSensor("D")

base.set_default_speed(12)
arm.set_default_speed(10)
claws.set_default_speed(20)

base.set_stop_action(Motor.HOLD)
arm.set_stop_action(Motor.HOLD)

colors = ["blue", "red", "yellow", "green", "violet"]

while True:
    base.run_to_position(90)
    claws.run_to_position(0)
    arm.run_to_position(60)

    color = sensor.get_color()

    if color == None or color not in colors:
        continue

    wait_for_seconds(3)

    arm.run_to_position(25)
    claws.run_to_position(140)
    # arm.run_to_position(15)
    # claws.run_to_position(135)
    arm.run_to_position(60)

    base.run_to_position(270)
    wait_for_seconds(0.5)

    arm.run_to_position(15)
    claws.run_to_position(0)
    arm.run_to_position(60)
