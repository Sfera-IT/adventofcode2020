#!/usr/bin/env python3

lines = open("input", "r").readlines()
pieces = list(list('.' + x.strip() + '.') for x in lines)
width = len(pieces[0])
pieces = [list('.' * width)] + pieces + [list('.' * width)]
height = len(pieces)


def deltas():
    for i in (-1, 0, 1):
        for j in (-1, 0, 1):
            for k in (-1, 0, 1):
                for w in (-1, 0, 1):
                    if (i, j, k, w) != (0, 0, 0, 0):
                        yield (i, j, k, w)


def neighbors(point):
    (a, b, c, d) = point
    for (i, j, k, w) in deltas():
        yield (a+i, b+j, c+k, d+w)


def cycle(states):
    updated = {}

    area = set()
    for point in states.keys():
        area.add(point)
        area.update(neighbors(point))
    
    for point in area:
        active_around = 0
        for other in neighbors(point):
            if states.get(other, False):
                active_around += 1
        if states.get(point, False):
            if (2 <= active_around <= 3):
                updated[point] = True
            else:
                updated[point] = False
        else:
            if active_around == 3:
                updated[point] = True
            else:
                updated[point] = False

        if not updated[point]:
            del updated[point]
    
    return updated



states = {}

for ri, r in enumerate(pieces):
    for ci, c in enumerate(r):
        if c == '#':
            states[(ri, ci, 0, 0)] = True


for a in range(6):
    states = cycle(states)


active = 0
for p in states:
    if states[p]:
        active += 1
print(active)
