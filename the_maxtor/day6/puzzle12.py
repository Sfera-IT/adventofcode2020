#!/usr/bin/python3

inputArray = []
tempArray = []
with open("input_day6.txt") as inputFile:
    for row in inputFile:
        if row != "\n":
            tempArray.append(row.strip())
        else:
            inputArray.append(tempArray)
            tempArray = []

if tempArray: inputArray.append(tempArray)
print(inputArray)

total = 0
for group in inputArray:
    tempGroup = group[0]
    for answer in tempGroup:
        for peopleAnswers in group[1:]:
            if type(peopleAnswers) is list:
                for personAnswers in peopleAnswers:
                    if answer not in personAnswers:
                        group[0] = group[0].replace(answer, "")
            else:
                if answer not in peopleAnswers:
                    group[0] = group[0].replace(answer, "")

for group in inputArray:
    total = total + len(group[0])

print(total)