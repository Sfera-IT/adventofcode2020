#!/usr/bin/env python3

lines = open("input", "r").readlines()
pieces = list(x.strip().split(' = ') for x in lines)


def apply(mask, value):
    converted = list(bin(value + 2**40)[-36:])
    for (i, c) in enumerate(mask):
        if c != 'X':
            converted[i] = c
    return int(''.join(converted), 2)


def run():
    mask = None
    memory = {}
    for line in pieces:
        if line[0].startswith('mask'):
            mask = line[1]
        if line[0].startswith('mem['):
            position = line[0].split('[')[1].split(']')[0]
            memory[position] = apply(mask, int(line[1]))
    return sum(memory.values())


print(run())
