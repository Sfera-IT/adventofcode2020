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

print(trees_in_slope(3, 1))
