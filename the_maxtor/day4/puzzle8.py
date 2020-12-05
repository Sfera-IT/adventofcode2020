#!/usr/bin/python3

import re

inputArray = []
parameters = {}
with open("input_day4.txt") as inputFile:
    for row in inputFile:
        if row != "\n":
            elements = row.strip().split(" ")
            for element in elements:
                key = str(element.split(":")[0])
                value = str(element.split(":")[1])
                parameters[key] = value
        else:
            inputArray.append(parameters)
            parameters = {}

if parameters:
    inputArray.append(parameters)

validPassports = 0
for parametersList in inputArray:
    if "byr" in parametersList.keys() and "iyr" in parametersList.keys() and "eyr" in parametersList.keys() \
       and "hgt" in parametersList.keys() and "hcl" in parametersList.keys() and "ecl" in parametersList.keys() \
       and "pid" in parametersList.keys():
        if 1920 <= int(parametersList["byr"]) <= 2002:
            if 2010 <= int(parametersList["iyr"]) <= 2020:
                if 2020 <= int(parametersList["eyr"]) <= 2030:
                    pattern = re.compile("^(\d{2,3})(in|cm$)")
                    hgt = pattern.match(parametersList["hgt"])
                    if hgt:
                        if (hgt.group(2) == "in" and (59 <= int(hgt.group(1)) <= 76)) or (hgt.group(2) == "cm" \
                           and (150 <= int(hgt.group(1)) <= 193)):
                            if re.match('^#[0-9a-f]{6}$', parametersList["hcl"]):
                                if re.match("^(amb|blu|brn|gry|grn|hzl|oth)$", parametersList["ecl"]):
                                    if re.match("^\d{9}$", parametersList["pid"]):
                                        validPassports = validPassports + 1

print(validPassports)
