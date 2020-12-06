#!/usr/bin/env python3

lines = open("input", "r").readlines()
pieces = list(x.strip() for x in lines)

def seat_id(code):
    rows = list(range(128))
    cols = list(range(8))
    for char in code:
        if char == 'F':
            rows = rows[:int(len(rows)/2)]
        if char == 'B':
            rows = rows[int(len(rows)/2):]
        if char == 'L':
            cols = cols[:int(len(cols)/2)]
        if char == 'R':
            cols = cols[int(len(cols)/2):]
    return rows[0]*8 + cols[0]

seats = list(map(seat_id, pieces))

holes = [
    i for i in range(100, 966) if i not in seats
]

print(holes)
