#!/usr/bin/env python3

import numpy

contents = open("input", "r").read()
blocks = [
    l for l in contents.split('\n\n')
]

player_1 = [
    int(l) for l in blocks[0].strip().split('\n')[1:]
]

player_2 = [
    int(l) for l in blocks[1].strip().split('\n')[1:]
]


while len(player_1) and len(player_2):
    one = player_1[0]
    two = player_2[0]
    if one > two:
        player_1 = player_1[1:] + [one, two]
        player_2 = player_2[1:]
    else:
        player_1 = player_1[1:]
        player_2 = player_2[1:] + [two, one]


winner = player_1 if len(player_1) else player_2
score = 0
for i in range(len(winner)):
    score += (len(winner) - i) * winner[i]
print(score)
