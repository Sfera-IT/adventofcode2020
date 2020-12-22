#!/usr/bin/env python3

from sage.arit.misc import CRT_list

lines = open("input2", "r").readlines()
moment = int(lines[0])
values = list(int(x) if x != 'x' else x for x in lines[1].split(','))

divisors = [
    -i for i, v in enumerate(values) if v != 'x'
]

# Sage function
c = CRT_list(divisors, [v for v in values if v != 'x'])
print(c)
