import re
from helpers import load_input

def sumGroups(values):
    sum = 0
    for group in values.split('\n\n'):
        gAnsw = set()
        for answ in group:
            if re.match(r'[a-z]', answ):
                gAnsw.add(answ)
        sum += len(gAnsw)
    return sum


def sumOnlyYES(values):
    sum = 0
    for group in values.split('\n\n'):
        candidates = []
        persons = group.splitlines()
        for person in persons:
            pAnsw = set([char for char in person])
            candidates.append(pAnsw)
        common = set.intersection(*candidates)
        sum += len(common)
    return sum


if __name__ == '__main__':
    values = load_input('./../data/6.txt')
    print(sumGroups(values))
    print(sumOnlyYES(values))
