import re
from collections import defaultdict

rule_re = re.compile("^([\w\s]+):\s(\d+)-(\d+) or (\d+)\-(\d+)$")


def solvePart1(fields, tickets):
    out_of_limits = []
    for ticket in tickets:
        numbers = [int(n) for n in ticket.split(",")]
        for number in numbers:
            found = False
            for field in fields:
                limits = fields[field]
                if len(fields[field]) == 4:
                    if (
                        limits[-4] <= number <= limits[-3]
                        or limits[-2] <= number <= limits[-1]
                    ):
                        found = True
            if not found:
                out_of_limits.append(number)
    return sum(out_of_limits)


def solvePart2(fields, myticket, tickets):
    valid_tickets = []
    for ticket in tickets:
        all_found = True
        numbers = [int(n) for n in ticket.split(",")]
        for number in numbers:
            found = False
            for field in fields:
                limits = fields[field]
                if len(fields[field]) == 4:
                    if (
                        limits[-4] <= number <= limits[-3]
                        or limits[-2] <= number <= limits[-1]
                    ):
                        found = True
                elif len(fields[field]) == 2:
                    if limits[-2] <= number <= limits[-1]:
                        found = True
            if not found:
                all_found = False
        if all_found:
            valid_tickets.append(ticket)
    valid_fields = defaultdict(set)

    for field in fields.keys():
        valid_fields[field] = set({x for x in range(len(fields.keys()))})

    for index in range(len(fields.keys())):
        for name in fields.keys():
            for ticket in valid_tickets:
                numbers = [int(n) for n in ticket.split(",")]
                number = numbers[index]
                limits = fields[name]
                if len(limits) == 4:
                    if not (
                        limits[-4] <= number <= limits[-3]
                        or limits[-2] <= number <= limits[-1]
                    ):
                        valid_fields[name].remove(index)
                        break
                elif len(limits) == 2:
                    if not limits[-2] <= number <= limits[-1]:
                        valid_fields[name].remove(index)
                        break

    positions_taken = set()
    while any(len(indices) > 1 for indices in valid_fields.values()):
        for field, positions in valid_fields.items():
            if len(positions - positions_taken) == 1:
                valid_fields[field] -= positions_taken
                positions_taken |= valid_fields[field]

    departure_fields = [
        position
        for name, positions in valid_fields.items()
        for position in positions
        if "departure" in name
    ]

    result = 1
    for departure in departure_fields:
        result *= int(myticket[departure])

    return result


def getPuzzleInput():
    fields = defaultdict(list)
    myticket = []
    tickets = []
    is_mine = False
    with open("./../data/16.txt") as input_txt:
        for line in input_txt:
            if rule_re.match(line.strip()):
                match = rule_re.match(line.strip())
                fields[match.group(1)] = [
                    int(match.group(2)),
                    int(match.group(3)),
                    int(match.group(4)),
                    int(match.group(5)),
                ]
            elif "your ticket" in line.strip():
                is_mine = True
            elif "nearby" in line.strip():
                continue
            elif is_mine:
                myticket = line.strip().split(",")
                is_mine = False
            else:
                if line.strip():
                    tickets.append(line.strip())
    return fields, myticket, tickets


if __name__ == "__main__":
    fields, myticket, tickets = getPuzzleInput()

    answer1 = solvePart1(fields, tickets)
    print(f"Res Part 1: {answer1}")

    answer2 = solvePart2(fields, myticket, tickets)
    print(f"Res Part 2: {answer2}")
