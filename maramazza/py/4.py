def createDictionaryFromEntry(entry):
    result = dict()

    entry = entry.replace(' ', '\n')
    entry = entry.split('\n')

    for info in entry:
        result[info[0:3]] = info[4:]

    return result


if __name__ == "__main__":
    data = []

    with open('./../data/4.txt', 'r') as f:
        data = f.read().split('\n\n')

    # part 1
    totPart1 = 0

    requiredFields = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']

    for entry in data:
        required = 0
        for field in requiredFields:
            if field in entry:
                required += 1
        if required >= len(requiredFields):
            totPart1 += 1

    print(f'Result Part 1: {totPart1}')

    # part 2
    totPart2 = 0

    for entry in data:
        entryDictionary = createDictionaryFromEntry(entry)

        valid = 0

        try:
            # byr
            byr = int(entryDictionary['byr'])
            if byr >= 1920 and byr <= 2002:
                valid += 1

            # iyr
            iyr = int(entryDictionary['iyr'])
            if iyr >= 2010 and iyr <= 2020:
                valid += 1

            # eyr
            eyr = int(entryDictionary['eyr'])
            if eyr >= 2020 and eyr <= 2030:
                valid += 1

            # hgt
            hgt = entryDictionary['hgt']

            if hgt.endswith('cm'):
                if int(hgt[:-2]) >= 150 and int(hgt[:-2]) <= 193:
                    valid += 1
            elif hgt.endswith('in'):
                if int(hgt[:-2]) >= 59 and int(hgt[:-2]) <= 76:
                    valid += 1
            else:
                pass

            # hcl
            hcl = entryDictionary['hcl']
            if hcl.startswith('#') and len(hcl) == 7:
                valid += 1
            int(hcl[1:], 16)

            #ecl
            ecl = entryDictionary['ecl']
            if ecl == 'amb' or ecl == 'blu' or ecl == 'brn' or ecl == 'gry' or \
               ecl == 'grn' or ecl == 'hzl' or ecl == 'oth':
                valid += 1

            # pid
            pid = entryDictionary['pid']
            if pid.isdigit() and len(pid) == 9:
                valid += 1
        except:
            valid = 0

        if valid >= 7:
            totPart2 += 1

    print(f'Result Part 2: {totPart2}')
