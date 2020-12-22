#!/usr/bin/env python3

contents = open("input", "r").read()
blocks = contents.split('\n\n')

range_lines = [
    line.strip().split(': ') for line in blocks[0].split('\n')
]

def parse_interval(value):
    results = []
    ranges = value.split(' or ')
    for r in ranges:
        x, y = map(int, r.split('-'))
        results += list(range(x, y + 1))
    return set(results)


intervals = {
    l[0]: parse_interval(l[1]) for l in range_lines
}

tickets = [
    list(map(int, l.strip().split(','))) for l in blocks[2].split('\n') if ',' in l
]


def errors(ticket):
    residuals = []
    for v in ticket:
        valid = False
        for k in intervals:
            if v in intervals[k]:
                valid = True
                break
        if not valid:
            residuals.append(v)
    return residuals


value = 0
for t in tickets:
    e = errors(t)
    for v in e:
        value = value + v

print(value)
