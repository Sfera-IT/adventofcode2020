#!/usr/bin/env python3

import numpy

contents = open("input", "r").read()
blocks = [
    l for l in contents.split('\n\n')
    if len(l)
]


def ordered(border):
    if border[::-1] < border:
        return border[::-1]
    return border


class Tile(object):
    def __init__(self, block):
        lines = block.split('\n')
        self.identifier = int(lines[0].split('Tile ')[1].split(':')[0])
        self.array = numpy.array([
            list(map(int, row.replace('#', '1').replace('.', '0')))
            for row in lines[1:] if len(row)
        ])
        self.borders = []
        self.borders.append(ordered(self.array[0, :].tolist()))
        self.borders.append(ordered(self.array[-1, :].tolist()))
        self.borders.append(ordered(self.array[:, 0].tolist()))
        self.borders.append(ordered(self.array[:, -1].tolist()))


    def __repr__(self):
        return f'Tile {self.identifier}\n{self.array}\n'

tiles = {}
for block in blocks:
    t = Tile(block)
    tiles[t.identifier] = t

identifiers = sorted(tiles.keys())
adjacent = {
    t: [] for t in tiles
}

for i in range(len(identifiers)):
    current = identifiers[i]
    tile = tiles[current]
    for k in range(len(identifiers)):
        if k == i:
            continue
        following = identifiers[k]
        other = tiles[following]
        for border in tile.borders:
            if border in other.borders:
                adjacent[current].append(following)

corners = []
for k in adjacent:
    row = adjacent[k]
    if len(row) < 3:
        corners.append(k)

if len(corners) == 4:
    result = 1
    for c in corners:
        result *= c
    print(result)
