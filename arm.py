# LEGO type:standard slot:16
from spike import Motor, ColorSensor
from spike.control import wait_for_seconds

base = Motor("A")
arm = Motor("B")
claws = Motor("C")
sensor = ColorSensor("D")

try:
    base.set_default_speed(15)
    arm.set_default_speed(10)
    claws.set_default_speed(20)

    base.set_stop_action(Motor.HOLD)
    arm.set_stop_action(Motor.HOLD)

    color_map = {
        "blue": 1,
        "red": 1,
        "yellow": 1,
        "green": 0,
        "violet": 0,
    }

    while True:
        base.run_to_position(0)
        claws.run_to_position(0)
        arm.run_to_position(15)

        color = sensor.get_color()
        
        if color == None or color not in color_map:
            continue

        claws.run_to_position(135)
        arm.run_to_position(45)
        
        if color_map[color] == 0:
            base.run_to_position(90)
            base.run_to_position(90)
        elif color_map[color] == 1:
            base.run_to_position(270)
            base.run_to_position(270)
        wait_for_seconds(0.5)

        arm.run_to_position(15)
        claws.run_to_position(0)
except (KeyboardInterrupt, SystemExit):
    claws.stop()
    base.stop()
    arm.stop()
    
    claws.run_to_position(0)
    base.run_to_position(0)
    arm.run_to_position(15)
    
    base.set_stop_action(Motor.BRAKE)
    arm.set_stop_action(Motor.BRAKE)
