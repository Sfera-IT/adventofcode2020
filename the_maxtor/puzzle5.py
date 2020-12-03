
inputArray = []
with open("input_day3.txt") as inputFile:
    for row in inputFile:
        inputArray.append(row.strip())

rowLength = len(inputArray[0])
iter = 0
trees = 0
for row in inputArray:
    if row[(3*iter)%rowLength] == '#':
        trees = trees+1
    iter = iter+1

print(trees)