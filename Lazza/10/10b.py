#!/usr/bin/env python3

lines = open("input", "r").readlines()
values = list(int(x) for x in lines)
values = [0] + sorted(values)
values = values + [values[-1] + 3]


cached = {}


def the_tail(values):
    k = tuple(values)
    if k in cached:
        return cached[k]
    else:
        result = subsets(values)
        cached[k] = result
        return result


def subsets(values):
    if len(values) < 3:
        return 1
    tail = the_tail(values[1:])
    if values[2] - values[0] <= 3:
        return tail + subsets([values[0]] + values[2:])
    else:
        return tail

print(subsets(values))
