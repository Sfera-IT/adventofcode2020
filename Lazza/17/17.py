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
                if (i, j, k) != (0, 0, 0):
                    yield (i, j, k)


def neighbors(point):
    (a, b, c) = point
    for (i, j, k) in deltas():
        yield (a+i, b+j, c+k)


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
        if not states.get(point, False):
            if active_around == 3:
                updated[point] = True
            else:
                updated[point] = False
    
    return updated


def take_point(x):
    return (x[2], x[0], x[1])


def show(states):
    out = set()
    for p in states:
        if states[p]:
            out.add(p)
    
    previous = None
    for p in sorted(out, key=take_point):
        if p[2] != previous:
            print('-', p[2], '-')
            previous = p[2]
        print(p)
    print()
    print()

states = {}

for ri, r in enumerate(pieces):
    for ci, c in enumerate(r):
        if c == '#':
            states[(ri, ci, 0)] = True


#show(states)
for a in range(6):
    #print(a)
    states = cycle(states)
    #show(states)

active = 0
for p in states:
    if states[p]:
        active += 1
print(active)
