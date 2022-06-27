# LEGO type:advanced slot:6 autostart
from spike.control import wait_for_seconds
from random import randint
from runtime.virtualmachine import VirtualMachine
import hub

sn_pos = (0, 0)
direction = 0
changed = False
got_apple = False
snake = []
apple = None


async def right_pressed(vm, stack):
    global direction, changed
    if changed:
        direction = (direction + 1) % 4
        changed = True


async def on_start(vm, stack):
    global sn_pos, direction, changed, got_apple, snake, apple

    while True:
        changed = False
        hub.display.clear()
        hub.display.pixel(sn_pos[0], sn_pos[1], 9)

        if direction in (0, 2):
            hub.display.pixel(sn_pos[0], sn_pos[1] - 1, 4)
            hub.display.pixel(sn_pos[0], sn_pos[1] + 1, 4)
        elif direction in (1, 3):
            hub.display.pixel(sn_pos[0] - 1, sn_pos[1], 4)
            hub.display.pixel(sn_pos[0] + 1, sn_pos[1], 4)

        for x, y in snake:
            hub.display.pixel(x, y, 9)

        for i in range(5):
            hub.display.pixel(4, i, 9)

        if not apple:
            if len(snake) < 19:
                apple = (randint(0, 3), randint(0, 4))
                while apple in snake or apple == sn_pos:
                    apple = (randint(0, 3), randint(0, 4))
            else:
                hub.led((0, 255, 0))
                break

        hub.display.pixel(apple[0], apple[1], 7)

        wait_for_seconds(0.5)

        snake.append(sn_pos)
        if not got_apple:
            snake.pop(0)
        got_apple = False

        if direction == 0:
            sn_pos = (sn_pos[0] + 1, sn_pos[1])
        elif direction == 1:
            sn_pos = (sn_pos[0], sn_pos[1] + 1)
        elif direction == 2:
            sn_pos = (sn_pos[0] - 1, sn_pos[1])
        elif direction == 3:
            sn_pos = (sn_pos[0], sn_pos[1] - 1)

        if sn_pos in snake:
            raise SystemExit

        if sn_pos == apple:
            apple = None
            got_apple = True

        if sn_pos[0] < 0 or sn_pos[0] >= 4 or sn_pos[1] < 0 or sn_pos[1] >= 5:
            raise SystemExit


def setup(rpc, system, stop):
    vm = VirtualMachine(rpc, system, stop, "snake")
    vm.register_on_start("snake_on_start", on_start)
    vm.register_on_button(
        "snake_on_right_pressed",
        right_pressed,
        "right",
        "pressed",
    )
    return vm
