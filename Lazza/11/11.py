#!/usr/bin/env python3

lines = open("input", "r").readlines()
pieces = list(list('.' + x.strip() + '.') for x in lines)
width = len(pieces[0])
pieces = [list('.' * width)] + pieces + [list('.' * width)]
height = len(pieces)

def next_grid(original):
    result = [
        list(r) for r in original
    ]
    for r in range(1, height-1):
        for c in range(1, width-1):
            char = original[r][c]
            if char not in 'L#':
                continue
            adjacent = [
                original[r-1][c-1],
                original[r-1][c],
                original[r-1][c+1],
                original[r][c-1],
                original[r][c+1],
                original[r+1][c-1],
                original[r+1][c],
                original[r+1][c+1]
            ]
            occupied = len([a for a in adjacent if a == '#'])
            if char == 'L' and occupied == 0:
                result[r][c] = '#'
            if char == '#' and occupied >= 4:
                result[r][c] = 'L'
    return result


def show(grid):
    for g in grid:
        print(g)


while True:
    new_grid = next_grid(pieces)
    if new_grid == pieces:
        break
    pieces = new_grid

print(sum([len([x for x in row if x == '#']) for row in pieces]))
