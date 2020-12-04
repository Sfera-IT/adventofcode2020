#!/usr/bin/python3

inputArray = []
with open("input_day3.txt") as inputFile:
    for row in inputFile:
        inputArray.append(row.strip())

rowLength = len(inputArray[0])
iter = 0
treesSlop1 = 0
treesSlop2 = 0
treesSlop3 = 0
treesSlop4 = 0
treesSlop5 = 0
for row in inputArray:
    if row[iter % rowLength] == '#':
        treesSlop1 = treesSlop1+1
    if row[(3*iter) % rowLength] == '#':
        treesSlop2 = treesSlop2+1
    if row[(5*iter) % rowLength] == '#':
        treesSlop3 = treesSlop3+1
    if row[(7*iter) % rowLength] == '#':
        treesSlop4 = treesSlop4+1
    if row[(int(iter / 2)) % rowLength] == '#' and iter % 2 == 0:
        treesSlop5 = treesSlop5+1
    iter = iter+1

result = treesSlop1*treesSlop2*treesSlop3*treesSlop4*treesSlop5
print(result)