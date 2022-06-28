# LEGO type:standard slot:18
from spike import Motor, ColorSensor
from spike.control import wait_for_seconds

base = Motor("A")
arm = Motor("B")
claws = Motor("C")
sensor = ColorSensor("D")

base.set_default_speed(10)
arm.set_default_speed(10)
claws.set_default_speed(20)

base.set_stop_action(Motor.HOLD)
arm.set_stop_action(Motor.HOLD)

left = ["green"]#, "cyan"]
right = ["red"]#, "yellow"]
al = left + right

while True:
    arm.run_to_position(55)
    claws.run_to_position(0)
    base.run_to_position(270)

    color = sensor.get_color()
    
    if color == None or color not in al:
        continue
    
    wait_for_seconds(3)
    
    arm.run_to_position(15)
    claws.run_to_position(140)
    arm.run_to_position(55)
    
    if color in left:
        base.run_to_position(0)
        base.run_to_position(0)
        base.run_to_position(0)
    elif color in right:
        base.run_to_position(180)
        base.run_to_position(180)
        base.run_to_position(180)
    wait_for_seconds(0.5)
    
    arm.run_to_position(15)
    claws.run_to_position(0)
    arm.run_to_position(55)
