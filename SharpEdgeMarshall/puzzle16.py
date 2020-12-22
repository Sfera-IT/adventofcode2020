import copy
import re

field_re = re.compile("^(.*):\s(\d+)-(\d+)\sor\s(\d+)-(\d+)$")
ticket_re = re.compile("^\d+(?:,|$)")

fields = {}
tickets = []
total = 0

with open('puzzle16.txt', 'r') as input_file:
    while True:
        line = input_file.readline()
        if not line:
            break
        else:
            line = line[:-1]
        field = field_re.match(line)
        ticket = ticket_re.match(line)

        if field:
            fields[field.group(1)] = [(int(field.group(2)),int(field.group(3))),(int(field.group(4)),int(field.group(5)))]
        elif ticket:
            tickets.append(list(map(int,line.split(","))))


# STAR 1
for ticket in tickets:
    for val in ticket:
        found = False
        for field in fields.values():
            for subfield in field:
                if subfield[0] <= val <= subfield[1]:
                    found = True
                    break
            if found:
                break
        if not found:
            total += val

print(total)

# STAR 2
ttickets = []
for ticket in tickets:
    valid = True
    for val in ticket:
        found = False
        for field in fields.values():
            for subfield in field:
                if subfield[0] <= val <= subfield[1]:
                    found = True
                    break
            if found:
                break
        if not found:
            valid = False
            break
    if valid:
        ttickets.append(ticket)

tickets = ttickets
maps = [None]*len(tickets[0])

for ticket in tickets:
    for tkey, val in enumerate(ticket):
        tfields = []
        for key, field in fields.items():
            for subfield in field:
                if subfield[0] <= val <= subfield[1]:
                    tfields.append(key)
                    break
        maps[tkey] = tfields if not maps[tkey] else list(set(maps[tkey]) & set(tfields))

comp_map = []

while True:
    found = False
    for tmap in maps:
        if len(tmap) == 1 and tmap[0] not in comp_map:
            found = True
            comp_map.append(tmap[0])
            for ttmap in maps:
                if tmap[0] in ttmap and len(ttmap) > 1:
                    ttmap.pop(ttmap.index(tmap[0]))
    if not found:
        break

res = 1
for tmap in maps:
    if "departure" in tmap[0]:
        res *= tickets[0][maps.index(tmap)]

print(res)

