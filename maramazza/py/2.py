totPart1 = 0
totPart2 = 0

with open('./../data/2.txt', 'r') as f:
    for line in f:
        # part 1

        rule = line.split(':')[0]
        password = line.split(':')[1]
        letter = rule[-1]
        quantity = rule.split()[0]
        quantity_low = quantity.split('-')[0]
        quantity_high = quantity.split('-')[1]

        if (password.count(letter) >= int(quantity_low)) and (password.count(letter) <= int(quantity_high)):
            totPart1 += 1

        # part 2

        first_pos = int(quantity_low)
        second_pos = int(quantity_high)

        if ((password[first_pos] == letter) and (password[second_pos] != letter)) or ((password[first_pos] != letter) and (password[second_pos] == letter)):
            totPart2 += 1

    print(f'Part 1: {totPart1}')
    print(f'Part 2: {totPart2}')
