import re


class Passport:
    _req_fields = {
        # byr (Birth Year) - four digits; at least 1920 and at most 2002.
        'byr': r'^(19[2-9][0-9]|200[0-2])$',
        # iyr (Issue Year) - four digits; at least 2010 and at most 2020.
        'iyr': r'^20(1[0-9]|20)$',
        # eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
        'eyr': r'^20(2[0-9]|30)$',
        # hgt (Height) - a number followed by either cm or in:
        # If cm, the number must be at least 150 and at most 193.
        # If in, the number must be at least 59 and at most 76.
        'hgt': r'^(1([5-8][0-9]|9[0-3])cm|(59|6[0-9]|7[0-6])in)$',
        # hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
        'hcl': r'^#[0-9a-f]{6}$',
        # ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
        'ecl': r'^(amb|blu|brn|gry|grn|hzl|oth)$',
        # pid (Passport ID) - a nine-digit number, including leading zeroes.
        'pid': r'^[0-9]{9}$',
    }

    def __init__(self, raw_str: str):
        self._raw = raw_str
        self._data = raw_str.split()

    def hasAllRequiredFields(self) -> bool:
        for fname in self._req_fields.keys():
            if (fname + ":") not in self._raw:
                return False
        return True

    def validateAll(self) -> bool:
        for datum in self._data:
            [key, val] = datum.split(':')
            if key not in self._req_fields:
                continue
            if not re.match(self._req_fields[key], val, flags=re.IGNORECASE):
                # print(val)
                # print(f"\nPassport: {self._raw} \nValidation failed {key}\t{val} does not match " + self._req_fields[key])
                return False
        return True

    def isValid(self) -> bool:
        return self.hasAllRequiredFields() and self.validateAll()


f = open("input/4.txt", "r")

data = re.sub(r'[\n\r]{2,}', '|', f.read().strip())

raw = ""
valid_list = []
for line in data.split('|'):
    pass_data = re.sub(r'[\r\n]+', ' ', line)
    p = Passport(re.sub(r'[\r\n]+', ' ', line))

    if p.isValid():
        valid_list.append(pass_data)

valid = len(valid_list)
print(f"Valid: {valid}")

f.close()
