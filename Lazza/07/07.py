#!/usr/bin/env python3

lines = open("input", "r").readlines()
rules = list(
    x.strip() for x in lines
    if 'contain no other' not in x and ' bag' in x
)

parents = {}

def bag_quantity(row):
    row = row.split(' bag')[0]
    pieces = row.split(' ')
    amount = int(pieces[0])
    name = ' '.join(pieces[1:])
    return (amount, name)


def parse(rule):
    pieces = rule.split(' bags contain ')
    parent = pieces[0]
    children = (bag_quantity(x.strip()) for x in pieces[1].split(','))
    for amount, name in children:
        if name in parents:
            parents[name][parent] = amount
        else:
            parents[name] = { parent: amount }


def containing(color):
    results = []
    if color not in parents:
        return results
    for name in parents[color].keys():
        results = results + [name] + containing(name)
    return results


for rule in rules:
    parse(rule)

color = 'shiny gold'
print(len(set(containing(color))))
