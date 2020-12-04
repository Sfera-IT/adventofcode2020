import re
input_file = open('puzzle4.txt', 'r')

filetext = input_file.read()
input_file.close()

sol_1 = re.compile("(?:(?:byr|hgt|eyr|ecl|pid|iyr|hcl):[^\s]+\s?(?:cid:[^\s]+\s?)?){7,}")
sol_2 = re.compile("(?:(?:byr:(19[2-8][0-9]|199[0-9]|200[0-2])|hgt:((1[5-8][0-9]|19[0-3])cm|(59|6[0-9]|7[0-6])in)|eyr:(202[0-9]|2030)|ecl:(amb|blu|brn|gry|grn|hzl|oth)|pid:[0-9]{9}|iyr:(201[0-9]|2020)|hcl:(#[a-f0-9]{6}))\s?(?:cid:[^\s]+\s?)?){7,}")

print(len(sol_1.findall(filetext)))
print(len(sol_2.findall(filetext)))
