#!/usr/bin/env python3

lines = open("input", "r").readlines()
commands = list(x.strip() for x in lines)

positions = ['E', 'S', 'W', 'N']
index = 0

coords = {
    'E': 0,
    'N': 0
}

def adjust(c, arg):
    if c in ('N', 'E'):
        coords[c] += arg
    if c == 'S':
        adjust('N', -arg)
    if c == 'W':
        adjust('E', -arg)

def run(command):
    global index
    c, arg = command[0], int(command[1:])
    if c in 'NESW':
        adjust(c, arg)
    if c == 'L':
        index -= int(arg/90)
        index = (index + 4) % 4
    if c == 'R':
        index += int(arg/90)
        index = index % 4
    if c == 'F':
        dir = positions[index]
        adjust(dir, arg)


for c in commands:
    run(c)
print(abs(coords['E']) + abs(coords['N']))
