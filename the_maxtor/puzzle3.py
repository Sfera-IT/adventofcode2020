
valid = 0
with open("input_day2.txt") as inputFile:
    for row in inputFile:
        policy, password = row.split(":")
        min = policy.split("-")[0]
        max = policy.split("-")[1].split(" ")[0]
        letter = policy.split("-")[1].split(" ")[1]
        occurances = password.strip().count(letter)
        if int(min) <= occurances <= int(max):
            valid = valid + 1
print(valid)