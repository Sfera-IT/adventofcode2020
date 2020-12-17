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


invalid = run()
stop = False

for i in range(0, len(values)):
    if stop:
        break
    for j in range(i+1, len(values)):
        subset = values[i:j]
        if sum(subset) == invalid:
            v_min = min(subset)
            v_max = max(subset)
            print(v_min + v_max)
            stop = True
            break
