#!/usr/bin/env python3

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


def game(player_1, player_2, idx = 1):
    previous_one = {}

    player_1 = tuple(player_1)
    player_2 = tuple(player_2)

    while len(player_1) and len(player_2):
        if ((player_1, player_2)) in previous_one:
            #print(idx, player_1, player_2, 'instant')
            return (1, player_1)
        previous_one[(player_1, player_2)] = True

        #print(idx, player_1, player_2)
        one = player_1[0]
        two = player_2[0]
        left_one = player_1[1:]
        left_two = player_2[1:]
        #print(one, two, left_one, left_two, len(left_one) >= one and len(left_two) >= two)
        if len(left_one) >= one and len(left_two) >= two:
            winner, deck = game(left_one[:one], left_two[:two], idx+1)
            if winner == 1:
                player_1 = player_1[1:] + (one, two)
                player_2 = player_2[1:]
            else:
                player_1 = player_1[1:]
                player_2 = player_2[1:] + (two, one)

        else:
            if one > two:
                player_1 = player_1[1:] + (one, two)
                player_2 = player_2[1:]
            else:
                player_1 = player_1[1:]
                player_2 = player_2[1:] + (two, one)

    if len(player_1):
        return (1, player_1)
    else:
        return (2, player_2)


winner_id, winner = (game(player_1, player_2))

score = 0
for i in range(len(winner)):
    score += (len(winner) - i) * winner[i]
print(score)
