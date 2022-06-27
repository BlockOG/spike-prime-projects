# LEGO type:standard slot:16
from spike import Motor, ColorSensor

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
        "yellow": 0,
        "green": 1,
        "violet": 1,
        "red": 1,
        "blue": 2,
    }

    while True:
        claws.run_to_position(0)
        base.run_to_position(0)

        arm.run_to_position(15)
        claws.run_to_position(135)

        color = sensor.get_color()

        arm.run_to_position(45)

        if color == None:
            continue
        elif color in color_map:
            base.run_to_position(color_map[color] * 90 + 90)
        else:
            continue

        arm.run_to_position(15)
        claws.run_to_position(0)
except KeyboardInterrupt:
    claws.stop()
    base.stop()
    arm.stop()
    
    claws.run_to_position(0)
    base.run_to_position(0)
    arm.run_to_position(15)
    
    base.set_stop_action(Motor.BRAKE)
    arm.set_stop_action(Motor.BRAKE)
