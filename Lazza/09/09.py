#!/usr/bin/env python3

lines = open("input", "r").readlines()
values = list(int(x) for x in lines)
window = 25


def valid(rotating, value):
    for k in rotating.keys():
        delta = value - k
        if delta != k and delta in rotating:
            return True
    return False


def run():
    for i in range(window, len(values)):
        rotating = {
            v: True for v in values[i-window:i]
        }
        if not valid(rotating, values[i]):
            return values[i]


print(run())
