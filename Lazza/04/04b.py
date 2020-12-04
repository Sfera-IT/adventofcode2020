#!/usr/bin/env python3

import re

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
    
    if ok:
        ok = ok and parsed['byr'].isdigit() and len(parsed['byr']) == 4 and 1920 <= int(parsed['byr']) <= 2002
        ok = ok and parsed['iyr'].isdigit() and len(parsed['iyr']) == 4 and 2010 <= int(parsed['iyr']) <= 2020
        ok = ok and parsed['eyr'].isdigit() and len(parsed['eyr']) == 4 and 2020 <= int(parsed['eyr']) <= 2030
        ok_cm = parsed['hgt'].endswith('cm') and parsed['hgt'][:-2].isdigit() and 150 <= int(parsed['hgt'][:-2]) <= 193
        ok_in = parsed['hgt'].endswith('in') and parsed['hgt'][:-2].isdigit() and 59 <= int(parsed['hgt'][:-2]) <= 76
        ok = ok and (ok_cm or ok_in)
        pattern = re.compile("^#[0123456789abcdef][0123456789abcdef][0123456789abcdef][0123456789abcdef][0123456789abcdef][0123456789abcdef]$")
        ok = ok and pattern.match(parsed['hcl'])
        ok = ok and parsed['ecl'] in ('amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth')
        ok = ok and len(parsed['pid']) == 9 and parsed['pid'].isdigit()
    return ok



count = 0
for p in passports:
    if valid(parse(p)):
        count = count + 1

print(count)
