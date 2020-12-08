#!/usr/bin/env python3

content = open("input", "r").read()
groups = content.replace('\r', '').replace('\n', ' ').split('  ')

def answers(group):
    return len(set(x for x in group if 'a' <= x <= 'z'))

count = 0
for g in groups:
    count = count + answers(g)

print(count)
