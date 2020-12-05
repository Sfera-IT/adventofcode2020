#!/usr/bin/python3

inputArray = []
parameters = []
with open("input_day4.txt") as inputFile:
    for row in inputFile:
        if row != "\n":
            elements = row.strip().split(" ")
            for element in elements:
                parameters.append(element.split(":")[0])
        else:
            inputArray.append(parameters)
            parameters = []

if parameters:
    inputArray.append(parameters)

validPassports = 0
basedOnLength = 0
for parametersList in inputArray:
    if len(parametersList) > 6:
        basedOnLength = basedOnLength + 1
    if "byr" in parametersList and "iyr" in parametersList and "eyr" in parametersList \
       and "hgt" in parametersList and "hcl" in parametersList and "ecl" in parametersList \
       and "pid" in parametersList:
        validPassports = validPassports + 1

print(basedOnLength)
print(validPassports)
