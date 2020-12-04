#!/usr/bin/python3

valid = 0
with open("input_day2.txt") as inputFile:
    for row in inputFile:
        policy, password = row.split(":")
        position1 = int(policy.split("-")[0])
        position2 = int(policy.split("-")[1].split(" ")[0])
        letter = policy.split("-")[1].split(" ")[1]
        if (password.strip()[position1-1] == letter and password.strip()[position2-1] != letter) or (password.strip()[position1-1] != letter and password.strip()[position2-1] == letter):
            valid = valid + 1
print(valid)