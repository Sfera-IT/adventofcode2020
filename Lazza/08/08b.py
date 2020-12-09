#!/usr/bin/env python3

import copy

lines = open("input", "r").readlines()
pieces = list(x.strip() for x in lines)


def parse(line):
    parts = line.split(' ')
    command = parts[0]
    arg = int(parts[1].replace('+', ''))
    return (command, arg)


def run(pieces):
    dirty = {}
    ip = 0
    acc = 0
    while True:
        if ip in dirty or ip < 0:
            return False
        if ip >= len(pieces):
            return acc
        dirty[ip] = True
        command, arg = parse(pieces[ip])
        if command == 'acc':
            acc = acc + arg
            ip = ip + 1
            continue
        if command == 'jmp':
            ip = ip + arg
            continue
        ip = ip + 1


for i in range(len(pieces)):
    cloned = copy.deepcopy(pieces)
    if cloned[i][:3] == 'jmp':
        cloned[i] = 'nop' + cloned[i][3:]
    elif cloned[i][:3] == 'nop':
        cloned[i] = 'jmp' + cloned[i][3:]
    executes = run(cloned)
    if executes != False:
        print(executes)
        break
