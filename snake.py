# LEGO type:standard slot:6 autostart
from spike.control import wait_for_seconds
from random import randint
import hub

sn_pos = (0, 0)
direction = 0
changed = False
got_apple = False
snake = []
apple = None

hub.button.left.callback(
    lambda time: (
        globals().__setitem__("direction", (direction - 1) % 4),
        globals().__setitem__("changed", True),
    )
    if time == 0 and not changed
    else None
)
hub.button.right.callback(
    lambda time: (
        globals().__setitem__("direction", (direction + 1) % 4),
        globals().__setitem__("changed", True),
    )
    if time == 0 and not changed
    else None
)

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

    if not apple:
        if len(snake) < 24:
            apple = (randint(0, 4), randint(0, 4))
            while apple in snake or apple == sn_pos:
                apple = (randint(0, 4), randint(0, 4))
        else:
            hub.led("green")
            while True:
                pass

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
        break

    if sn_pos == apple:
        apple = None
        got_apple = True

    if sn_pos[0] < 0 or sn_pos[0] >= 5 or sn_pos[1] < 0 or sn_pos[1] >= 5:
        break

hub.display.clear()
raise SystemExit
