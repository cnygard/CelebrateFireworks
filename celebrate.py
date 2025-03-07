import sys
import time
import random
import math
import subprocess
import sys

# it's possible to use ansi to determine screen width

if len(sys.argv) < 2:
  print("Usage: python3 celebrate <program>")
  exit(1)

# run the program and capture stdout
process = subprocess.Popen(
    sys.argv[1:],
    stdout=subprocess.PIPE
)
oks = 0
fails = 0

for line in process.stdout:
  decoded = line.decode("utf-8")
  oks += decoded.count("ok")
  fails += decoded.count("FAIL")
  print(decoded)

# calculate number of fireworks
num_fireworks = 5
if oks + fails > 0:
  num_fireworks = int((oks / (oks + fails)) * 5)

# prep colors
defaultcolor = "\033[49"
numcolors = 10
colors = ["\033[41","\033[42","\033[43", "\033[44"]
colors = []
for i in range(numcolors):
  colors.append("\033[4" + str((i%7)+1))

# terminal writing functions
def write_color(color):
  sys.stdout.write(color)
  sys.stdout.write('m ')
  move_left(1)

def move_up(n):
  sys.stdout.write("\033["+ str(n) + "A")

def move_down(n):
  sys.stdout.write("\033[" + str(n) + "B")

def move_right(n):
  sys.stdout.write("\033["+ str(n) + "C")

def move_left(n):
  sys.stdout.write("\033["+ str(n) + "D")

move_up(1)

# save initial cursor position
sys.stdout.write("\0337")

locations = []

class Firework:
  def __init__(self, pos, height, size):
    self.pos = pos
    self.height = height
    self.size = size
    self.offset = 0

for i in range(num_fireworks):
  locations.append(Firework(pos=random.randrange(i*20+5, i*20+15), height=random.randrange(5,20), size=random.randrange(4,7)))

# draw firework trails
for i in range(20):
  for l in locations:
    if i > l.height:
      continue
    move_right(l.pos)
    write_color("\033[43")
    r = random.randrange(20)
    if r < 5:
      move_left(1)
      l.pos -= 1
    if r > 14:
      move_right(1)
      l.pos += 1
    time.sleep(0.01)
    sys.stdout.flush()
    move_left(l.pos)
  move_up(1)

sys.stdout.write("\0338")

time.sleep(0.3)
sys.stdout.flush()

# draw explosions
seed = random.randrange(100000)
for i in range(10):
  for l in locations:
    centerw = l.size * 2 - 1
    centerh = l.size
    width = centerw * 2 - 1 
    height = centerh * 2 - 1
    move_right(l.pos - centerw)
    move_up(l.height + centerh)
    for y in range(height):
      for x in range(width):
        write_color(defaultcolor)
        if math.sqrt(((x-centerw)**2)/4 + (y-centerh)**2) < l.size and random.randrange(100000) % 3 == 0:
          write_color(random.choice(colors))
        move_right(1)
      move_down(1)
      move_left(width)
      time.sleep(0.005)
      sys.stdout.flush()
    sys.stdout.write("\0338")

# reset cursor to original position
sys.stdout.write("\0338")
move_down(1)
