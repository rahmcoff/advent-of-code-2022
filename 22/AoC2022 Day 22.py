#!/bin/python3

from io import StringIO
import re

testdata = """        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5"""

moves = None
field = []

joins = {}


def join(edge1, edge2, dir1, dir2):
    r1 = iter(edge1)
    r2 = iter(edge2)
    while True:
        try:
            p1 = next(r1)
            p2 = next(r2)
        except StopIteration:
            break
        joins[(p1, dir1)] = (p2, dir2)
        joins[(p2, (dir2 + 2) % 4)] = (p1, (dir1 + 2) % 4)


def ground(pos):
    return field[pos[0]][pos[1]]


def neigh(pos, dir):
    if (pos, dir) in joins:
        return joins[(pos, dir)]
    w = len(field[0])
    h = len(field)
    if dir == 0:  # right
        return ((pos[0], (pos[1] + 1) % w), dir)
    elif dir == 1:  # down
        return (((pos[0] + 1) % h, pos[1]), dir)
    elif dir == 2:  # left
        return ((pos[0], (pos[1] - 1) % w), dir)
    elif dir == 3:  # up
        return (((pos[0] - 1) % h, pos[1]), dir)
    else:  # default
        return (pos, dir)


def move(pos, dir):
    n, ndir = neigh(pos, dir)
    if ground(n) == " ":
        while ground(n) == " ":
            n, ndir = neigh(n, ndir)
    
    if ground(n) == "#":
        return (pos, dir)
    
    return (n, ndir)


with open("input.txt", 'r') as f:
    # with StringIO(testdata) as f:
    while l := f.readline():
        if l[0] == '\n':
            continue
        elif l[0].isnumeric():
            moves_orig = l
        else:
            field.append(l[:-1])

width = max(map(len, field))
field = [" " * (width + 2), *[f" {l}".ljust(width + 2) for l in field], " " * (width + 2)]

start = (1, field[1].find('.'))
pos = start
moves = moves_orig
dir = 0


def dir_to_arrow(dir_num: int):
    if dir_num == 0:
        return '>'
    elif dir_num == 1:
        return 'v'
    elif dir_num == 2:
        return '<'
    elif dir_num == 3:
        return '^'


while m := re.match(r"(\d+)(.*)", moves):
    moves = m.group(2)
    for _ in range(int(m.group(1))):
        field[pos[0]] = field[pos[0]][:pos[1]] + dir_to_arrow(dir) + field[pos[0]][pos[1]+1:]
        pos, dir = move(pos, dir)
    if m := re.match(r"([RL])(.*)", moves):
        moves = m.group(2)
        if m.group(1) == "R":
            dir = (dir + 1) % 4
        elif m.group(1) == "L":
            dir = (dir - 1) % 4
        else:
            raise Exception(f"Unknown direction token: {m.group(1)}")
    else:
        print(f"No more direction tokens, remaining string: '{moves}'")

print(dir, pos)
print(1000 * pos[0] + 4 * pos[1] + dir)
for line in field:
    print(line)

# join to cube (hardcoded)

#       a    b
#     f        c
#            d
#     g    d
#   g
# f        c
#        e
# a    e
#   b

# a
join([(1, x) for x in range(51, 101)], [(y, 1) for y in range(151, 201)], 3, 0)
# b
join([(1, x) for x in range(101, 151)], [(200, x) for x in range(1, 51)], 3, 3)
# c
join([(y, 150) for y in range(1, 51)], [(y, 100) for y in range(150, 100, -1)], 0, 2)
# d
join([(50, x) for x in range(101, 151)], [(y, 100) for y in range(51, 101)], 1, 2)
# e
join([(150, x) for x in range(51, 101)], [(y, 50) for y in range(151, 201)], 1, 2)
# f
join([(y, 1) for y in range(101, 151)], [(y, 51) for y in range(50, 0, -1)], 2, 0)
# g
join([(101, x) for x in range(1, 51)], [(y, 51) for y in range(51, 101)], 3, 0)

pos = start
dir = 0
moves = moves_orig

while m := re.match(r"(\d+)(.*)", moves):
    moves = m.group(2)
    for _ in range(int(m.group(1))):
        pos, dir = move(pos, dir)
    if m := re.match(r"([RL])(.*)", moves):
        moves = m.group(2)
        if m.group(1) == "R":
            dir = (dir + 1) % 4
        elif m.group(1) == "L":
            dir = (dir - 1) % 4
        else:
            raise Exception(f"Unknown direction token: {m.group(1)}")
    else:
        print(f"No more direction tokens, remaining string: '{moves}'")

print(dir, pos)
print(1000 * pos[0] + 4 * pos[1] + dir)
