# LEGO type:standard slot:8 autostart
from spike.control import wait_for_seconds
import hub

pos = 0

ball_pos = (2, 2)
ball_speed = (1, 1)

hub.button.left.callback(
    lambda time: globals().__setitem__("pos", pos - 1)
    if pos >= 0 and time == 0
    else None
)
hub.button.right.callback(
    lambda time: globals().__setitem__("pos", pos + 1)
    if pos <= 0 and time == 0
    else None
)

while True:
    hub.display.clear()
    hub.display.pixel(ball_pos[0], ball_pos[1], 9)

    if ball_pos[0] in (0, 1):
        hub.display.pixel(0, 0, 9)
    if ball_pos[0] in (0, 1, 2):
        hub.display.pixel(1, 0, 9)
    hub.display.pixel(2, 0, 9)
    if ball_pos[0] in (2, 3, 4):
        hub.display.pixel(3, 0, 9)
    if ball_pos[0] in (3, 4):
        hub.display.pixel(4, 0, 9)

    if pos == -1:
        hub.display.pixel(0, 4, 9)
    if pos in (-1, 0):
        hub.display.pixel(1, 4, 9)
    hub.display.pixel(2, 4, 9)
    if pos in (0, 1):
        hub.display.pixel(3, 4, 9)
    if pos == 1:
        hub.display.pixel(4, 4, 9)

    wait_for_seconds(0.5)

    if ball_pos[0] in (0, 4):
        ball_speed = (-ball_speed[0], ball_speed[1])

    if (
        (ball_pos[0] == 2 and ball_pos[1] == 3)
        or ball_pos[1] == 1
        or (pos in (0, 1) and ball_pos[1] == 3 and ball_pos[0] == 3)
        or (pos in (-1, 0) and ball_pos[1] == 3 and ball_pos[0] == 1)
    ):
        ball_speed = (ball_speed[0], -ball_speed[1])

    ball_pos = (ball_pos[0] + ball_speed[0], ball_pos[1] + ball_speed[1])
    
    if ball_pos[1] > 4:
        raise SystemExit
