import re
input_file = open("puzzle7.txt", "r")

# STAR 1

matches = set()

search_for = ['shiny gold bag']

mapping = {}

for i in input_file:
 
    phase1 = re.match("^(.*?)s contain (.*).$", i)
    container = phase1.group(1)
    phase2 = re.findall("\d (.*?)s?(?:,|$)", phase1.group(2))
    mapping[container] = phase2

while search_for:
    bag = search_for.pop()
    for container,contains in mapping.items():
        if bag in contains:
            matches.add(container)
            search_for.append(container)

print(len(matches))

# STAR 2

input_file.seek(0)

search_for = 'shiny gold bag'

for i in input_file:
 
    phase1 = re.match("^(.*?)s contain (.*).$", i)
    container = phase1.group(1)
    phase2 = re.findall("(\d+) (.*?)s?(?:,|$)", phase1.group(2))
    mapping[container] = phase2
    print(phase2)

def find_deep(search):
    contains = mapping[search]
    b_sum = 0
    for bag in contains:
        b_sum += int(bag[0]) + (int(bag[0]) * find_deep(bag[1]))
    
    return b_sum 


print(find_deep(search_for))
