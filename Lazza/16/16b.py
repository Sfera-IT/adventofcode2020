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


valid = []
for t in tickets:
    e = errors(t)
    if not len(e):
        valid.append(t)


columns = [
    set(r[i] for r in valid) for i in range(len(valid[0]))
]

possible = {}
for col in range(len(columns)):
    for k in intervals:
        i = intervals[k]
        if columns[col].issubset(i):
            if col in possible:
                possible[col].append(k)
            else:
                possible[col] = [k]


sure = {}

while len(sure.keys()) < len(intervals.keys()):
    label = None
    for key in possible:
        if len(possible[key]) == 1:
            label = possible[key][0]
            sure[label] = key
            break
    for key in possible:
        possible[key] = [l for l in possible[key] if l != label]


my_ticket = list(map(int, blocks[1].split('\n')[1].split(',')))


product = 1
for label in sure:
    if label.startswith('departure'):
        product *= my_ticket[sure[label]]

print(product)
