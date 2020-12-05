#!/usr/bin/env python3

content = open("input", "r").read()
passports = content.replace('\r', '').replace('\n', ' ').split('  ')

def parse(passport):
    fields = (x.split(':') for x in passport.split(' ') if ':' in x)
    return {
        k: t for (k, t) in fields
    }

def valid(parsed):
    keys = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']
    ok = True
    for k in keys:
        ok = ok and k in parsed
    return ok


count = 0
for p in passports:
    if valid(parse(p)):
        count = count + 1

print(count)
