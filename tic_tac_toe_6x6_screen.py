# LEGO type:advanced slot:1
from spike import ForceSensor
from spike.control import wait_for_seconds
from runtime.virtualmachine import VirtualMachine
import hub


class Image3x3:
    def __init__(self, port, string="000000000"):
        self.string = string
        self.port = port
    
    def pixel(self, x: int, y: int, value: int=None):
        if 0 <= x <= 2 and 0 <= y <= 2:
            if value is None:
                return int(self.string[x + y * 3])
            else:
                self.string = self.string[:x + y * 3] + str(value) + self.string[x + y * 3 + 1:]
    
    async def show(self, vm, delay=1, clear=False):
        await vm.system.display.show_image_string_async(self.string, port=self.port, delay=delay, clear=clear)


class Image6x6:
    def __init__(self, port1, port2, port3, port4, string="000000000:000000000:000000000:000000000"):
        string = string.split(":")
        
        self.images = [
            Image3x3(port1, string[0]),
            Image3x3(port2, string[1]),
            Image3x3(port3, string[2]),
            Image3x3(port4, string[3]),
        ]
    
    def pixel(self, x: int, y: int, value: int = None):
        if 0 <= x <= 2:
            if 0 <= y <= 2:
                self.images[0].pixel(x, y, value)
            elif 3 <= y <= 5:
                self.images[2].pixel(x, y - 3, value)
        elif 3 <= x <= 5:
            if 0 <= y <= 2:
                self.images[1].pixel(x - 3, y, value)
            elif 3 <= y <= 5:
                self.images[3].pixel(x - 3, y - 3, value)
    
    def rect(self, x1: int, y1: int, x2: int, y2: int, value: int):
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                self.pixel(x, y, value)
    
    async def show(self, vm, delay=1, clear=False):
        for j, i in enumerate(self.images):
            await i.show(vm, delay, clear)


class Image6x6_3x3(Image6x6):
    def pixel(self, x: int, y: int, value: int):
        super().pixel(x * 2    , y * 2    , value)
        super().pixel(x * 2 + 1, y * 2    , value)
        super().pixel(x * 2    , y * 2 + 1, value)
        super().pixel(x * 2 + 1, y * 2 + 1, value)


grid = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]
chosen = [0, 0]
turn = 0
color_map = [0, 6, 9, 3]
won = False
who_won = 0
button = ForceSensor("E")
screen = Image6x6_3x3("A", "B", "C", "D")


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
            grid[chosen[1]][chosen[0]] = who_won + 1
            
            wait_for_seconds(0.5)
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
    
    hub.led(color_map[turn + 1])


async def on_button_hard_pressed(vm, stack):
    global won, who_won, turn, chosen
    if not grid[chosen[1]][chosen[0]]:
        screen.pixel(chosen[0], chosen[1], color_map[turn + 1])
        grid[chosen[1]][chosen[0]] = turn + 1
        
        turn = abs(turn - 1)
        hub.led(color_map[turn + 1])
        
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
