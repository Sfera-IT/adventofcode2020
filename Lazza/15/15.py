#!/usr/bin/env python3

values = [0, 13, 16, 17, 1, 10, 6]

current = values[-1]

positions = {
    v: [i+1] for i, v in enumerate(values)
}

iteration = 1
for v in values:
    #print(iteration, '->', v)
    iteration += 1

while iteration <= 2020:
    if current not in positions or len(positions[current]) < 2:
        current = 0
    else:
        pos = list(positions[current])
        current = pos[0] - pos[1]
    positions[current] = [iteration] + positions.get(current, [])[:1]
    #print(iteration, '->', current)
    iteration += 1

print(current)
