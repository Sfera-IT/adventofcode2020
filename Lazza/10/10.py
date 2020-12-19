#!/usr/bin/env python3

lines = open("input", "r").readlines()
values = list(int(x) for x in lines)
values = [0] + sorted(values)

deltas = [
    values[i+1]-values[i] for i in range(len(values)-1)
] + [3]

count_one = len([d for d in deltas if d == 1])
count_three = len([d for d in deltas if d == 3])

print(count_one * count_three)
