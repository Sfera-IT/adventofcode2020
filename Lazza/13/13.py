#!/usr/bin/env python3

import math

lines = open("input", "r").readlines()
moment = int(lines[0])
values = list(int(x) for x in lines[1].split(',') if x != 'x')

moments = {
    math.ceil(moment / v) * v - moment: v for v in values
}

k = min(moments.keys())
print(moments[k] * k)
