#!/usr/bin/python3

import re

def getBags(bag, rules):
    bags = []
    for rule in rules.keys():
        if bag in rules[rule]:
            bags.append(rule)
    return bags



bagRules = {}
with open("input_day7.txt") as inputFile:
    for row in inputFile:
        bagFinder = re.compile("\w*\s\w*\sbag")
        rule = bagFinder.findall(row.strip())
        outerBag = rule[0].split("bag")[0].strip()
        bagRules[outerBag] = []
        for bag in rule[1:]:
            bagRules[outerBag].append(bag.split("bag")[0].strip())

MYBAG = "shiny gold"
matchingBags = getBags(MYBAG, bagRules)
tempBags = matchingBags
while tempBags:
    for bag in tempBags:
        tempBags = getBags(bag,bagRules)
        if tempBags: matchingBags.extend(tempBags)

print(len(dict.fromkeys(matchingBags).keys()))