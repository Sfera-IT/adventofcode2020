#!/usr/bin/env python3

lines = open("input01", "r").readlines()
numbers = list(int(x.strip()) for x in lines)

indexed = {
    k: True for k in numbers
}

def summing_to(value):
    for n in numbers:
        if value-n in indexed:
            return [n, value-n]

value = 2020

for n in numbers:
    delta = value-n
    candidates = summing_to(delta)
    if candidates:
        print(n, candidates, n * candidates[0] * candidates[1])
        break
