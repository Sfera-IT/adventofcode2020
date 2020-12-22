#!/usr/bin/env python3

lines = open("input", "r").readlines()
commands = list(x.strip() for x in lines)

positions = ['E', 'S', 'W', 'N']
index = 0

coords = {
    'E': 0,
    'N': 0
}

point = {
    'E': 10,
    'N': 1
}

def adjust(c, arg):
    if c in ('N', 'E'):
        point[c] += arg
    if c == 'S':
        adjust('N', -arg)
    if c == 'W':
        adjust('E', -arg)

def run(command):
    global index
    global point
    c, arg = command[0], int(command[1:])
    if c in 'NESW':
        adjust(c, arg)
    if c == 'L':
        for i in range(int(arg/90)):
            e = -point['N']
            n = point['E']
            point = {
                'E': e,
                'N': n
            }
    if c == 'R':
        for i in range(int(arg/90)):
            e = point['N']
            n = -point['E']
            point = {
                'E': e,
                'N': n
            }
    if c == 'F':
        coords['E'] += (point['E']) * arg
        coords['N'] += (point['N']) * arg


for c in commands:
    run(c)

print(abs(coords['E']) + abs(coords['N']))
