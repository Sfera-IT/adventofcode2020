#!/usr/bin/env python3

import numpy

contents = open("input2", "r").read()
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
        self.borders.append(ordered(self.top()))
        self.borders.append(ordered(self.bottom()))
        self.borders.append(ordered(self.left()))
        self.borders.append(ordered(self.right()))

    def top(self):
        return self.array[0, :].tolist()

    def bottom(self):
        return self.array[-1, :].tolist()

    def left(self):
        return self.array[:, 0].tolist()

    def right(self):
        return self.array[:, -1].tolist()

    def adapt(self, top=None, left=None, right=None, bottom=None, invariant=False):
        valid = False
        tick = 0
        iterations = 0

        while not valid:
            self_top = self.top()
            self_left = self.left()
            self_right = self.right()
            self_bottom = self.bottom()
            if invariant:
                self_top = ordered(self_top)
                self_left = ordered(self_left)
                self_right = ordered(self_right)
                self_bottom = ordered(self_bottom)

            valid = (
                (top is None or self_top == top) and
                (left is None or self_left == left) and
                (right is None or self_right == right) and
                (bottom is None or self_bottom == bottom)
            )
            if not valid:
                if tick:
                    self.array = numpy.flip(self.array, 0)
                else:
                    self.array = numpy.rot90(self.array)
                tick = 1-tick
                iterations += 1

            if iterations > 8:
                return False

        return True

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


# Initialize the image map and place the first three elements
length = int(len(blocks) ** 0.5)
image_map = [
    [None] * length
    for _ in range(length)
]
remaining = set(identifiers)

image_map[0][0] = corners[0]
image_map[0][1] = adjacent[corners[0]][0]
image_map[1][0] = adjacent[corners[0]][1]


tile = tiles[corners[0]]
other_right = tiles[adjacent[corners[0]][0]]
common_right = None
for border in tile.borders:
    if border in other_right.borders:
        common_right = border
        break
other_bottom = tiles[adjacent[corners[0]][1]]
common_bottom = None
for border in tile.borders:
    if border in other_bottom.borders:
        common_bottom = border
        break


tile.adapt(right=common_right, bottom=common_bottom, invariant=True)
other_right.adapt(left=tile.right())
other_bottom.adapt(top=tile.bottom())

remaining.remove(image_map[0][0])
remaining.remove(image_map[0][1])
remaining.remove(image_map[1][0])

adjacent = {
    t: set(adjacent[t])
    for t in adjacent
}

corners = [
    c for c in corners if c in remaining
]

iterations = 0
while len(remaining) > 0:
    iterations += 1
    print(iterations, '-> ', image_map)
    for r in range(length):
        for c in range(length):
            if image_map[r][c]:
                continue

            prev_top = image_map[r-1][c] if r > 0 else None
            prev_left = image_map[r][c-1] if c > 0 else None

            is_corner = (r == 0 and c == length-1) or (r == length-1 and c == 0)
            current_list = corners if is_corner else remaining

            candidates = []
            #print(is_corner_adjacent)
            for identifier in current_list:
                near = adjacent[identifier]
                potential = (prev_left is None or prev_left in near) and (prev_top is None or prev_top in near)
                if potential:
                    candidates.append(identifier)

            if len(candidates) > 0:
                filtered_candidates = []
                for identifier in candidates:
                    candidate = tiles[identifier]
                    common_left = tiles[prev_left].right() if prev_left else None
                    common_top = tiles[prev_top].bottom() if prev_top else None
                    if candidate.adapt(left=common_left, top=common_top):
                        filtered_candidates.append(identifier)
                
                if len(filtered_candidates) == 1:
                    identifier = filtered_candidates[0]
                    image_map[r][c] = identifier
                    remaining.remove(identifier)

print(image_map)
