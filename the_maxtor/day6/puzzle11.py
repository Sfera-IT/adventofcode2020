#!/usr/bin/python3

questions = []
totalYes = 0
with open("input_day6.txt") as inputFile:
    for row in inputFile:
        if row != "\n":
            for character in row.strip():
                if character not in questions:
                    questions.append(character)
        else:
            totalYes = totalYes + len(questions)
            questions = []

if questions: totalYes = totalYes + len(questions)

print(totalYes)