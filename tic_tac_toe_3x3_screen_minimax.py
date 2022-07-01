# LEGO type:advanced slot:2
from spike import ForceSensor
from spike.control import wait_for_seconds
from runtime.virtualmachine import VirtualMachine
import hub


class Image3x3:
    def __init__(self, port, string="000000000"):
        self.string = string
        self.port = port

    def __str__(self):
        return self.string

    __repr__ = __str__

    def pixel(self, x: int, y: int, value: int = None):
        if 0 <= x <= 2 and 0 <= y <= 2:
            if value is None:
                return int(self.string[x + y * 3])
            else:
                self.string = (
                    self.string[: x + y * 3] + str(value) + self.string[x + y * 3 + 1 :]
                )

    async def show(self, vm, delay=1, clear=False):
        await vm.system.display.show_image_string_async(
            str(self), port=self.port, delay=delay, clear=clear
        )


grid = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]
chosen = [0, 0]
color_map = [0, 6, 9, 3]
won = False
who_won = 0
button = ForceSensor("A")
screen = Image3x3("B")


def check_grid():
    for i in range(3):
        if grid[i][0] == grid[i][1] == grid[i][2] and grid[i][0]:
            return True, grid[i][0] - 1
        if grid[0][i] == grid[1][i] == grid[2][i] and grid[0][i]:
            return True, grid[0][i] - 1

    if (grid[0][0] == grid[1][1] == grid[2][2] and grid[1][1]) or (
        grid[2][0] == grid[1][1] == grid[0][2] and grid[1][1]
    ):
        return True, grid[1][1] - 1

    if all([y for x in grid for y in x]):
        return True, 2

    return False, 0


def move_chosen(move):
    if move > 1:
        move = 1
    if move < -1:
        move = -1

    chosen[0] += move

    if chosen[0] < 0:
        chosen[0] = 2
        chosen[1] -= 1
        if chosen[1] < 0:
            chosen[1] = 2
    elif chosen[0] > 2:
        chosen[0] = 0
        chosen[1] += 1
        if chosen[1] > 2:
            chosen[1] = 0


def move_chosen_no(move, check=[0]):
    global chosen
    pchosen = chosen.copy()

    move_chosen(move)

    while grid[chosen[1]][chosen[0]] not in check:
        move_chosen(move)

        if chosen == pchosen:
            return False

    return True


def show_grid():
    for x in range(3):
        for y in range(3):
            screen.pixel(x, y, color_map[grid[y][x]])


async def stop_game(vm):
    global chosen
    hub.led(color_map[who_won + 1])
    wait_for_seconds(0.5)

    chosen = [2, 2]
    if who_won != 2:
        a = [0, 1, 2]
        a.pop(a.index(who_won + 1))
        while move_chosen_no(1, a):
            screen.pixel(chosen[0], chosen[1], color_map[who_won + 1])
            await screen.show(vm)
            wait_for_seconds(0.5)

            if chosen == [2, 2]:
                break
    else:
        for _ in range(9):
            move_chosen(1)
            screen.pixel(chosen[0], chosen[1], color_map[who_won + 1])
            await screen.show(vm)
            wait_for_seconds(0.5)

    vm.stop()


async def on_left_button_pressed(vm, stack):
    show_grid()
    if move_chosen_no(-1):
        screen.pixel(chosen[0], chosen[1], color_map[3])

    await screen.show(vm)


async def on_right_button_pressed(vm, stack):
    show_grid()
    if move_chosen_no(1):
        screen.pixel(chosen[0], chosen[1], color_map[3])

    await screen.show(vm)


async def on_start(vm, stack):
    screen.pixel(chosen[0], chosen[1], color_map[3])
    await screen.show(vm)

    hub.led(color_map[1])


def minimax(depth, is_maximizing):
    if depth > 5:
        return 0

    won, who_won = check_grid()
    if won:
        if who_won == 0:
            return -1
        elif who_won == 1:
            return 1
        elif who_won == 2:
            return 0

    if is_maximizing:
        best_score = -800
        for x in range(3):
            for y in range(3):
                if grid[y][x] == 0:
                    grid[y][x] = 2
                    score = minimax(depth + 1, False)
                    grid[y][x] = 0
                    if score > best_score:
                        best_score = score
        return best_score
    else:
        best_score = 800
        for x in range(3):
            for y in range(3):
                if grid[y][x] == 0:
                    grid[y][x] = 1
                    score = minimax(depth + 1, True)
                    grid[y][x] = 0
                    if score < best_score:
                        best_score = score
        return best_score


async def on_button_hard_pressed(vm, stack):
    global won, who_won, chosen

    screen.pixel(chosen[0], chosen[1], color_map[1])
    grid[chosen[1]][chosen[0]] = 1

    if move_chosen_no(1):
        screen.pixel(chosen[0], chosen[1], color_map[3])

    await screen.show(vm)

    if c := check_grid():
        won, who_won = c

        if won:
            await stop_game(vm)

    screen.pixel(chosen[0], chosen[1], color_map[0])

    best_score = -800
    went = False

    for x in range(3):
        for y in range(3):
            if grid[y][x] == 0:
                went = True
                grid[y][x] = 2
                score = minimax(0, False)
                grid[y][x] = 0
                if score > best_score:
                    best_score = score
                    chosen = [x, y]

    if went:
        screen.pixel(chosen[0], chosen[1], color_map[2])
        grid[chosen[1]][chosen[0]] = 2

    if move_chosen_no(1):
        screen.pixel(chosen[0], chosen[1], color_map[3])

    await screen.show(vm)

    if c := check_grid():
        won, who_won = c

        if won:
            await stop_game(vm)


def setup(rpc, system, stop):
    vm = VirtualMachine(rpc, system, stop, "tic_tac_toe")
    vm.register_on_start("tic_tac_toe_on_start", on_start)
    vm.register_on_button(
        "tic_tac_toe_on_left_pressed",
        on_left_button_pressed,
        "left",
        "pressed",
    )
    vm.register_on_button(
        "tic_tac_toe_on_right_pressed",
        on_right_button_pressed,
        "right",
        "pressed",
    )
    vm.register_on_condition(
        "tic_tac_toe_on_button_hard_pressed",
        on_button_hard_pressed,
        lambda vm, stack: button.get_force_newton() > 5,
    )
    return vm
