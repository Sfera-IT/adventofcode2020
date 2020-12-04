#!/usr/bin/env python3

lines = open("input02", "r").readlines()
pieces = list(x.split(' ') for x in lines)
ok = 0

def valid(password, a, b, l):
    first = password[a-1]
    second = password[b-1]
    return (first != second) and l in (first, second)

for line in pieces:
    min_, max_ = (int(k) for k in line[0].split('-'))
    letter = line[1][0]
    password = line[2]
    if valid(password, min_, max_, letter):
        ok = ok + 1

print(ok)

