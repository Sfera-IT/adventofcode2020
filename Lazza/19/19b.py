#!/usr/bin/env python3

import re

contents = open("input", "r").read()
blocks = contents.split('\n\n')

rule_lines = [
    line.strip().split(': ') for line in blocks[0].split('\n')
]

rules = dict(rule_lines)
rules['8'] = '42 | 42 8'
rules['11'] = '42 31 | 42 11 31'

strings = [
    line.strip() for line in blocks[1].split('\n') if len(line.strip())
]

max_len = max(map(len, strings))


def regex(rule_id):
    if rule_id == '8':
        partial = regex('42')
        return f'({partial}+)'
    
    if rule_id == '11':
        # Cheating a little bit
        partial_42 = regex('42')
        partial_31 = regex('31')
        result = ''
        for i in range(1, int(max_len / 2) + 1):
            result += '(' + partial_42 * i + partial_31 * i + ')|'
        return f'({result[:-1]})'

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
