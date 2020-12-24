#!/usr/bin/env python3

import re

contents = open("input", "r").read()
blocks = contents.split('\n\n')

rule_lines = [
    line.strip().split(': ') for line in blocks[0].split('\n')
]

rules = dict(rule_lines)

strings = [
    line.strip() for line in blocks[1].split('\n') if len(line.strip())
]

def regex(rule_id):
    rule = rules[rule_id]
    if rule.startswith('"'):
        return rule[1]
    
    parts = rule.split(' | ')
    result = ''
    for part in parts:
        partial = ''
        children = part.split(' ')
        for c in children:
            partial += regex(c)
        result += f'({partial})|'
    return f'({result[:-1]})'


pattern = '^' + regex('0') + '$'

amount = 0
for s in strings:
    if re.match(pattern, s):
        amount += 1

print(amount)
