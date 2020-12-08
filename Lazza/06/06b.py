#!/usr/bin/env python3

content = open("input", "r").read()
groups = content.replace('\r', '').replace('\n', ' ').split('  ')

def answers(group):
    words = [
        w for w in group.split(' ')
        if len(w) > 0
    ]
    if not len(words):
        return 0
    result = 0
    for letter in words[0]:
        partial = 0
        for word in words:
            if letter in word:
                partial = partial + 1
        if partial == len(words):
            result = result + 1
    return result

count = 0
for g in groups:
    count = count + answers(g)

print(count)
