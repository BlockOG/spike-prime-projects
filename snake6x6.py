# LEGO type:advanced slot:6
from runtime.virtualmachine import VirtualMachine
from random import randint
from time import time_ns
from spike.control import wait_for_seconds


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
                return self.images[0].pixel(x, y, value)
            elif 3 <= y <= 5:
                return self.images[2].pixel(x, y - 3, value)
        elif 3 <= x <= 5:
            if 0 <= y <= 2:
                return self.images[1].pixel(x - 3, y, value)
            elif 3 <= y <= 5:
                return self.images[3].pixel(x - 3, y - 3, value)
    
    def rect(self, x1: int, y1: int, x2: int, y2: int, value: int):
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                self.pixel(x, y, value)
    
    async def show(self, vm, delay=1, clear=False):
        for j, i in enumerate(self.images):
            await i.show(vm, delay, clear)


screen = Image6x6("A", "B", "C", "D")

snake_pos = [0, 0]
snake = []
direction = 0
changed = False
wrap = False

apple_pos = None
apple = False

color_map = [0, 6, 9]
ptime = time_ns()


async def on_start(vm, stack):
    screen.pixel(snake_pos[0], snake_pos[1], color_map[1])
    await screen.show(vm)


async def on_apple_pos_none(vm, stack):
    global apple_pos
    apple_pos = [randint(0, 5), randint(0, 5)]
    while apple_pos in snake or apple_pos == snake_pos:
        apple_pos = [randint(0, 5), randint(0, 5)]
    
    screen.pixel(apple_pos[0], apple_pos[1], color_map[2])
    await screen.show(vm)


def get_update(vm, stack):
    global ptime
    if (c := time_ns()) - ptime >= 500_000_000:
        ptime = c
        return True
    return False


async def update(vm, stack):
    global direction, changed, apple, apple_pos
    snake.append(snake_pos.copy())
    if not apple:
        a = snake.pop(0)
        screen.pixel(a[0], a[1], color_map[0])
    apple = False
    
    for i in snake:
        screen.pixel(i[0], i[1], color_map[1])
    
    if direction == 0:
        snake_pos[0] += 1
        if wrap:
            snake_pos[0] %= 6
    elif direction == 2:
        snake_pos[0] -= 1
        if wrap:
            snake_pos[0] %= 6
    elif direction == 1:
        snake_pos[1] += 1
        if wrap:
            snake_pos[1] %= 6
    elif direction == 3:
        snake_pos[1] -= 1
        if wrap:
            snake_pos[1] %= 6
    changed = False
    
    if snake_pos in snake or not 0 <= snake_pos[0] <= 5 or not 0 <= snake_pos[1] <= 5:
        screen.rect(0, 0, 5, 5, color_map[2])
        await screen.show(vm)
        wait_for_seconds(1)
        vm.stop()
    
    if snake_pos == apple_pos:
        apple_pos = None
        apple = True
        if len(snake) == 35:
            wait_for_seconds(1)
            vm.stop()
    
    screen.pixel(snake_pos[0], snake_pos[1], color_map[1])
    await screen.show(vm)


async def on_left_pressed(vm, stack):
    global direction, changed
    if not changed:
        direction -= 1
        direction %= 4
        changed = True


async def on_right_pressed(vm, stack):
    global direction, changed
    if not changed:
        direction += 1
        direction %= 4
        changed = True


def setup(rpc, system, stop):
    vm = VirtualMachine(rpc, system, stop, "6x6_snake")
    vm.register_on_start("6x6_snake_on_start", on_start)
    
    vm.register_on_condition(
        "6x6_snake_on_apple_pos_none",
        on_apple_pos_none,
        lambda vm, stack: apple_pos is None,
    )
    vm.register_on_condition(
        "6x6_snake_update",
        update,
        get_update,
    )
    
    vm.register_on_button(
        "6x6_snake_on_left_pressed",
        on_left_pressed,
        "left",
        "pressed",
    )
    vm.register_on_button(
        "6x6_snake_on_right_pressed",
        on_right_pressed,
        "right",
        "pressed",
    )
    
    return vm
