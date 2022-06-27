# LEGO type:standard slot:16
from spike import Motor, ColorSensor, PrimeHub
from spike.control import wait_for_seconds

base = Motor("A")
arm = Motor("B")
claws = Motor("C")
sensor = ColorSensor("D")

base.set_default_speed(15)
arm.set_default_speed(10)
claws.set_default_speed(20)

base.set_stop_action(Motor.HOLD)
arm.set_stop_action(Motor.HOLD)

while True:
    claws.run_to_position(0)
    arm.run_to_position(45)

    base.run_to_position(0)

    arm.run_to_position(15)
    claws.run_to_position(135)
    
    color = sensor.get_color()
    
    arm.run_to_position(45)

    if color == None:
        break
    elif color in ("red", "green", "violet"):
        base.run_to_position(180)
    elif color in ("blue"):
        base.run_to_position(90)
    elif color in ("yellow"):
        base.run_to_position(270)
    else:
        break

    arm.run_to_position(15)
    claws.run_to_position(0)
    arm.run_to_position(45)

base.set_stop_action(Motor.BRAKE)
arm.set_stop_action(Motor.BRAKE)
claws.run_to_position(0)
arm.run_to_position(15)
