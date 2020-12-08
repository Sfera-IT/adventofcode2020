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
    parents[parent] = {}
    for amount, name in children:
        parents[parent][name] = amount


def containing(color):
    results = 1
    if color not in parents:
        return results
    for name in parents[color].keys():
        results = results + parents[color][name] * containing(name)
    return results


for rule in rules:
    parse(rule)


color = 'shiny gold'
print(containing(color) - 1)
