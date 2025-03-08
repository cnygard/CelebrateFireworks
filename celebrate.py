import sys
import time
import random
import math
import subprocess
from typing import final
from enum import Enum
# it's possible to use ansi to determine screen width


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


@final
class Firework:
    def __init__(self, i: int):
        self.pos = random.randrange(i * 20 + 5, i*20+15)
        self.height = random.randrange(5, 20)
        self.size = random.randrange(4, 7)
        self.offset = 0


def write_color(color: str):  # terminal writing functions
    _ = out.write(color)
    _ = out.write('m ')
    move(1, Direction.LEFT)


def move(n: int, dir: Direction):
    off = ""
    match dir:
        case Direction.UP: off = "A"
        case Direction.DOWN: off = "B"
        case Direction.RIGHT: off = "C"
        case Direction.LEFT: off = "D"
    _ = out.write("\033[" + str(n) + off)


if len(sys.argv) < 2:
    sys.exit("Usage: python3 celebrate <program>")

# run the program and capture stdout
process = subprocess.Popen(
    sys.argv[1:],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

oks = 0
fails = 0

for line in process.stdout or []:
    decoded = line.decode("utf-8")
    oks += decoded.count("ok")
    fails += decoded.count("FAIL")
    print(decoded, flush=True)

# calculate number of fireworks
num_fireworks = 5
if oks + fails > 0:
    num_fireworks = int((oks / (oks + fails)) * 5)

# prep colors
# foreground
WHITE = "\0337"
# background
YELLOW = "\033[43"
DEFAULT = "\033[49"

NUMCOLORS = 10
colors: list[str] = ["\033[41", "\033[42", "\033[43", "\033[44"]
# Generate Background color ANSI codes
for i in range(NUMCOLORS):
    colors.append("\033[4" + str((i % 7)+1))

out = sys.stdout
move(1, Direction.UP)
# save initial cursor position
_ = out.write(WHITE)

locations: list[Firework] = []

for i in range(num_fireworks):
    locations.append(Firework(i))
# draw firework trails
for i in range(20):
    for loc in locations:
        if i > loc.height:
            continue
        move(loc.pos, Direction.RIGHT)
        write_color(YELLOW)
        r = random.randrange(20)
        if r < 5:
            move(1, Direction.LEFT)
        loc.pos -= 1
        if r > 14:
            move(1, Direction.RIGHT)
        loc.pos += 1
        time.sleep(0.01)
        _ = out.flush()
        move(loc.pos, Direction.LEFT)
    move(1, Direction.UP)

_ = out.write("\0338")

time.sleep(0.3)
_ = out.flush()

# draw explosions
for _ in range(6):
    for loc in locations:
        centerw = loc.size * 2 - 1
        centerh = loc.size
        width = centerw * 2 - 1
        height = centerh * 2 - 1
        move(loc.pos - centerw, Direction.RIGHT)
        move(loc.height + centerh, Direction.UP)
        for y in range(height):
            for x in range(width):
                seed = random.randrange(4783847) % 13
                write_color(DEFAULT)
                dimensions = (x - centerw)**2/4 + (y - centerh)**2
                if math.sqrt(dimensions) < loc.size - 1 and seed % 3 == 0:
                    write_color(random.choice(colors))
                move(1, Direction.RIGHT)
            move(1, Direction.DOWN)
            move(width, Direction.LEFT)
            time.sleep(0.008)
            _ = out.flush()
        _ = out.write("\0338")

# reset cursor to original position
_ = out.write("\0338")
move(1, Direction.DOWN)
