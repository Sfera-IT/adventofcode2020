#!/usr/bin/env python3

lines = open("input", "r").readlines()
pieces = list(x.strip() for x in lines)


def parse(line):
    parts = line.split(' ')
    command = parts[0]
    arg = int(parts[1].replace('+', ''))
    return (command, arg)


def run():
    dirty = {}
    ip = 0
    acc = 0
    while True:
        if ip in dirty:
            return acc
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


print(run())
