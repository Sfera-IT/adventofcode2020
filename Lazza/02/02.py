#!/usr/bin/env python3

lines = open("input02", "r").readlines()
pieces = list(x.split(' ') for x in lines)
ok = 0

for line in pieces:
    min_, max_ = (int(k) for k in line[0].split('-'))
    letter = line[1][0]
    password = line[2]
    count = len(''.join(l for l in password if l == letter))
    if min_ <= count <= max_:
        ok = ok + 1

print(ok)

