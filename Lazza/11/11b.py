#!/usr/bin/env python3

lines = open("input", "r").readlines()
pieces = list(list('.' + x.strip() + '.') for x in lines)
width = len(pieces[0])
pieces = [list('.' * width)] + pieces + [list('.' * width)]
height = len(pieces)


def get_adjacent(original, r, c):
    results = ['.'] * 8
    w = len(original[0])
    h = len(original)

    i = 1
    while r-i > 0 and c-i > 0 and original[r-i][c-i] == '.':
        i = i + 1
    results[0] = original[r-i][c-i]

    i = 1
    while r-i > 0 and original[r-i][c] == '.':
        i = i + 1
    results[1] = original[r-i][c]

    i = 1
    while r-i > 0 and c+i < w-1 and original[r-i][c+i] == '.':
        i = i + 1
    results[2] = original[r-i][c+i]

    i = 1
    while c-i > 0 and original[r][c-i] == '.':
        i = i + 1
    results[3] = original[r][c-i]

    i = 1
    while c+i < w-1 and original[r][c+i] == '.':
        i = i + 1
    results[4] = original[r][c+i]

    i = 1
    while r+i < h-1 and c-i > 0 and original[r+i][c-i] == '.':
        i = i + 1
    results[5] = original[r+i][c-i]

    i = 1
    while r+i < h-1 and original[r+i][c] == '.':
        i = i + 1
    results[6] = original[r+i][c]

    i = 1
    while r+i < h-1 and c+i < w-1 and original[r+i][c+i] == '.':
        i = i + 1
    results[7] = original[r+i][c+i]

    return results



def next_grid(original):
    result = [
        list(r) for r in original
    ]
    for r in range(1, height-1):
        for c in range(1, width-1):
            char = original[r][c]
            if char not in 'L#':
                continue
            adjacent = get_adjacent(original, r, c)
            occupied = len([a for a in adjacent if a == '#'])
            if char == 'L' and occupied == 0:
                result[r][c] = '#'
            if char == '#' and occupied >= 5:
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
