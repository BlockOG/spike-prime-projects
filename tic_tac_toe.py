# LEGO type:advanced slot:1
from spike.control import wait_for_seconds
from runtime.virtualmachine import VirtualMachine
from hub import display


grid = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]
chosen = [0, 0]
turn = 0
color_map = [3, 5, 7, 9]
won = False
who_won = 0


def check_grid():
    for i in range(3):
        if grid[i][0] == grid[i][1] == grid[i][2] and grid[i][0]:
            return True, grid[i][0] - 1
        if grid[0][i] == grid[1][i] == grid[2][i] and grid[0][i]:
            return True, grid[0][i] - 1

    if (
        grid[0][0] == grid[1][1] == grid[2][2]
        and grid[1][1]
    ) or (
        grid[2][0] == grid[1][1] == grid[0][2]
        and grid[1][1]
    ):
        return True, grid[1][1] - 1

    if all([y for x in grid for y in x]):
        return True, 2

    return False, 0


def move_chosen(move):
    if move > 1: move = 1
    if move < -1: move = -1
    
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
            display.pixel(x + 1, y + 1, color_map[grid[y][x]])


async def stop_game(vm):
    global chosen
    display.pixel(4, 4, color_map[who_won + 1])
    wait_for_seconds(0.5)
    
    chosen = [2, 2]
    if who_won != 2:
        a = [0, 1, 2]
        a.pop(a.index(who_won + 1))
        while move_chosen_no(1, a):
            display.pixel(chosen[0] + 1, chosen[1] + 1, color_map[who_won + 1])
            grid[chosen[1]][chosen[0]] = who_won + 1
            
            wait_for_seconds(0.5)
    else:
        for _ in range(9):
            move_chosen(1)
            display.pixel(chosen[0] + 1, chosen[1] + 1, color_map[who_won + 1])
            wait_for_seconds(0.5)

    vm.stop()


async def on_right_button_pressed(vm, stack):
    show_grid()
    if move_chosen_no(1):
        display.pixel(chosen[0] + 1, chosen[1] + 1, color_map[3])


async def on_left_button_pressed(vm, stack):
    global won, who_won, turn, chosen
    if not grid[chosen[1]][chosen[0]]:
        display.pixel(chosen[0] + 1, chosen[1] + 1, color_map[turn + 1])
        grid[chosen[1]][chosen[0]] = turn + 1
        
        turn = abs(turn - 1)
        display.pixel(4, 4, color_map[turn + 1])
        
        if move_chosen_no(1):
            display.pixel(chosen[0] + 1, chosen[1] + 1, color_map[3])

    if c := check_grid():
        won, who_won = c

        if won:
            await stop_game(vm)


async def on_start(vm, stack):
    show_grid()
    
    display.pixel(chosen[0] + 1, chosen[1] + 1, color_map[3])
    display.pixel(4, 4, color_map[turn + 1])


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
    return vm
