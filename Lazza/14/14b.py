#!/usr/bin/env python3

lines = open("input", "r").readlines()
pieces = list(x.strip().split(' = ') for x in lines)


def positions(value):
    for i in range(len(value)):
        if value[i] == 'X':
            copy1 = list(value)
            copy2 = list(value)
            copy1[i] = '0'
            copy2[i] = '1'
            return positions(copy1) + positions(copy2)
    return [value]


def apply(mask, value):
    converted = list(bin(value + 2**40)[-36:])
    for (i, c) in enumerate(mask):
        if c in ('1', 'X'):
            converted[i] = c
    return [int(''.join(a), 2) for a in positions(converted)]

def run():
    mask = None
    memory = {}
    for line in pieces:
        if line[0].startswith('mask'):
            mask = line[1]
        if line[0].startswith('mem['):
            position = int(line[0].split('[')[1].split(']')[0])
            positions = apply(mask, position)
            for p in positions:
                memory[p] = int(line[1])
    return sum(memory.values())


print(run())
