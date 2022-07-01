# LEGO type:advanced slot:1
from spike import ForceSensor
from spike.control import wait_for_seconds
from hub import display
from runtime.virtualmachine import VirtualMachine

chosen = [0, 0]
turn = 0
vertical = False
color_map = [0, 5, 7, 9]
won = False
who_won = 0
button = ForceSensor("A")
button2 = ForceSensor("B")


def check_grid():
    for i in range(3):
        if display.pixel(0, i) == display.pixel(1, i) == display.pixel(
            2, i
        ) and display.pixel(0, i):
            return True, color_map.index(display.pixel(0, i)) - 1
        if display.pixel(i, 0) == display.pixel(i, 1) == display.pixel(
            i, 2
        ) and display.pixel(i, 0):
            return True, color_map.index(display.pixel(i, 0)) - 1

    if (
        display.pixel(0, 0) == display.pixel(1, 1) == display.pixel(2, 2)
        and display.pixel(1, 1)
    ) or (
        display.pixel(0, 2) == display.pixel(1, 1) == display.pixel(2, 0)
        and display.pixel(1, 1)
    ):
        return True, color_map.index(display.pixel(1, 1)) - 1

    if all([display.pixel(x, y) for x in range(3) for y in range(3)]):
        return True, 2


def stop_game(vm):
    wait_for_seconds(0.5)
    display.pixel(3, 0, color_map[who_won + 1])
    wait_for_seconds(0.5)
    display.pixel(3, 1, color_map[who_won + 1])
    wait_for_seconds(0.5)
    display.pixel(3, 2, color_map[who_won + 1])
    wait_for_seconds(0.5)
    display.pixel(3, 3, color_map[who_won + 1])
    wait_for_seconds(0.5)
    display.pixel(2, 3, color_map[who_won + 1])
    wait_for_seconds(0.5)
    display.pixel(1, 3, color_map[who_won + 1])
    wait_for_seconds(0.5)
    display.pixel(0, 3, color_map[who_won + 1])
    wait_for_seconds(0.5)

    vm.stop()


async def left_callback(vm, stack):
    if vertical:
        display.pixel(4, chosen[1], 0)
        chosen[1] = min(chosen[1] + 1, 2)
        display.pixel(4, chosen[1], 9)
    else:
        display.pixel(chosen[0], 4, 0)
        chosen[0] = max(chosen[0] - 1, 0)
        display.pixel(chosen[0], 4, 9)


def button_hard_pressed(vm, stack):
    return button.get_force_newton() > 5


async def center_callback(vm, stack):
    global vertical, turn, chosen, won, who_won
    if vertical:
        vertical = False
        display.pixel(4, 3, 0)
        display.pixel(3, 4, 9)
    else:
        vertical = True
        display.pixel(3, 4, 0)
        display.pixel(4, 3, 9)


async def right_callback(vm, stack):
    if vertical:
        display.pixel(4, chosen[1], 0)
        chosen[1] = max(chosen[1] - 1, 0)
        display.pixel(4, chosen[1], 9)
    else:
        display.pixel(chosen[0], 4, 0)
        chosen[0] = min(chosen[0] + 1, 2)
        display.pixel(chosen[0], 4, 9)


async def on_start(vm, stack):
    display.pixel(chosen[0], 4, 9)
    display.pixel(4, chosen[1], 9)

    display.pixel(4, 4, color_map[turn + 1])

    display.pixel(3, 4, 9)


async def color_sensor_white(vm, stack):
    global won, who_won, turn, chosen
    if not display.pixel(*chosen):
        display.pixel(chosen[0], chosen[1], color_map[turn + 1])

        turn = abs(turn - 1)
        display.pixel(4, 4, color_map[turn + 1])

    if c := check_grid():
        won, who_won = c

        if won:
            stop_game(vm)


def setup(rpc, system, stop):
    vm = VirtualMachine(rpc, system, stop, "tic_tac_toe")
    vm.register_on_start("tic_tac_toe_on_start", on_start)
    vm.register_on_button(
        "tic_tac_toe_on_left_pressed",
        left_callback,
        "left",
        "pressed",
    )
    vm.register_on_condition(
        "tic_tac_toe_on_button_hard_pressed",
        center_callback,
        button_hard_pressed,
    )
    vm.register_on_button(
        "tic_tac_toe_on_right_pressed",
        right_callback,
        "right",
        "pressed",
    )
    vm.register_on_condition(
        "tic_tac_toe_on_color_white",
        color_sensor_white,
        lambda vm, stack: button2.get_force_newton() > 5,
    )
    return vm
