#!/usr/bin/env python3

lines = open("input01", "r").readlines()
numbers = list(int(x.strip()) for x in lines)

indexed = {
    k: True for k in numbers
}

for n in numbers:
    if 2020-n in indexed:
        print(n, '*', 2020-n, '->', n*(2020-n))
        break
