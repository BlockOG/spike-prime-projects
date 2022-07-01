# LEGO type:advanced slot:0
from spike import Motor, ColorSensor, ForceSensor, LightMatrix
from runtime.virtualmachine import VirtualMachine

# thrower = Motor("A")
# mover = Motor("B")
# button = ForceSensor("C")
# color_sensor = ColorSensor("D")
light_matrix = LightMatrix()

score = 0


async def loop():
    mover.set_default_speed(20)
    while True:
        mover.run_for_rotations(-0.5)
        mover.run_for_rotations(0.5)


async def on_start(vm, stack):
    with open("/projects/.slots") as f:
        slots = eval(f.read())

    with open("/projects/{}/__init__.mpy".format(slots[15]["id"]), "rb") as f:
        print(f.read())

    light_matrix.write(score)

    await loop()
    # vm.store.motor_speed("B", 148)
    # while True:
    #     a, b = vm.store.motor_acceleration("B")
    #     vm.store.motor_last_status(
    #         "B",
    #         vm.system.motors.on_port("B").run_for_degrees_async,
    #         129,
    #         52,
    #         vm.store.motor_speed("B"),
    #         stall = vm.store.motor_stall("B"),
    #         stop = vm.store.motor_stop("B"),
    #         acceleration = a,
    #         deceleration = b,
    #     )


def get_force_hard_pressed(vm, stack):
    return button.get_force_newton() > 5


async def on_force_hard_pressed(vm, stack):
    thrower.run_for_degrees(360, speed=1000)


def get_color_white(vm, stack):
    return color_sensor.get_color() == "white"


async def on_color_white(vm, stack):
    global score
    score += 1
    light_matrix.write(score)


def setup(rpc, system, stop):
    vm = VirtualMachine(rpc, system, stop, "basket_bot")
    vm.register_on_start("basket_bot_on_start", on_start)
    vm.register_on_condition(
        "basket_bot_on_force_sensor_hard_pressed",
        on_force_hard_pressed,
        get_force_hard_pressed,
    )
    vm.register_on_condition(
        "basket_bot_on_color_sensor_white",
        on_color_white,
        get_color_white,
    )
    return vm
