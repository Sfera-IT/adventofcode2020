#!/usr/bin/env python3

lines = open("input03", "r").readlines()
pieces = list(x.strip() for x in lines)

def trees_in_slope(right, down):
    trees = 0
    index = 0
    for line in pieces[down::down]:
        index = (index + right) % len(line)
        if line[index] == '#':
            trees = trees + 1
    return trees

results = 1
tuples = [
    (1, 1),
    (3, 1),
    (5, 1),
    (7, 1),
    (1, 2)
]

for t1, t2 in tuples:
    results = results * trees_in_slope(t1, t2)

print(results)
