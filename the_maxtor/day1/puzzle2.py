#!/usr/bin/python3

inputArray = []
with open("input_day1.txt") as inputFile:
    for row in inputFile:
        inputArray.append(int(row.strip()))

WANTED_RESULT = 2020

item1 = ''
item2 = ''
item3 = ''
for fixedItem in inputArray:
    for fixedItem2 in inputArray:
        for movingItem in inputArray:
            if fixedItem + fixedItem2 + movingItem == WANTED_RESULT:
                item1 = fixedItem
                item2 = fixedItem2
                item3 = movingItem

print (item1*item2*item3)

