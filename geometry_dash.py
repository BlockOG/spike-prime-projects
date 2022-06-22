# LEGO type:standard slot:9 autostart
import hub
from spike.control import wait_for_seconds

hub.button.left.was_pressed()
hub.button.right.was_pressed()

player_pos = [0, 4]
player_speed = [0.4, 0]
on_ground = True
blocks = [
    [0, 4, 4],
    [0, 5, 4],
    [0, 6, 4],
    [0, 7, 4],
    [0, 8, 4],
    [0, 9, 4],
    [0, 10, 4],
    [0, 11, 4],
    [1, 7, 3],
    [1, 8, 3],
]

jump = lambda: (
    globals().__setitem__(
        "player_speed",
        [player_speed[0], 0.5 if on_ground else player_speed[1]],
    ),
    globals().__setitem__("on_ground", False),
)

while True:
    img = hub.Image()
    if 4 >= round(player_pos[1]) >= 0:
        img.set_pixel(0, round(player_pos[1]), 7)

    for i in blocks:
        if 4 >= i[1] - round(player_pos[0]) >= 0:
            if i[0] == 0:
                img.set_pixel(i[1] - round(player_pos[0]), i[2], 9)
            elif i[0] == 1:
                img.set_pixel(i[1] - round(player_pos[0]), i[2], 5)

    hub.display.show(img)
    wait_for_seconds(0.1)

    player_pos[0] += player_speed[0]
    player_pos[1] -= player_speed[1]

    for i in blocks:
        if (
            player_pos[0] < i[1] + 1
            and player_pos[0] + 1 > i[1]
            and player_pos[1] < i[2] + 1
            and player_pos[1] + 1 > i[2]
        ):
            if i[0] == 0:
                if player_pos[1] - i[2] + 1 <= 0.25:
                    player_pos[1] = i[2] - 1
                    player_speed[1] = 0
                    on_ground = True
                else:
                    raise SystemExit
            elif i[0] == 1:
                raise SystemExit

    if player_pos[1] >= 4:
        player_pos[1] = 4
        player_speed[1] = 0
        on_ground = True

    player_speed[1] -= 0.1
    if player_speed[1] < -0.25:
        player_speed[1] = -0.25

    if hub.button.left.was_pressed() or hub.button.right.was_pressed():
        jump()
