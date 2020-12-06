import re
from helpers import load_input


def sum_groups(answers):
    sum = 0
    for group in answers.split('\n\n'):
        g_answ = set()
        for answ in group:
            if re.match(r'[a-z]', answ):
                g_answ.add(answ)
        sum += len(g_answ)
    return sum


def sum_only_yes(answers):
    sum = 0
    for group in answers.split('\n\n'):
        candidates = []
        persons = group.splitlines()
        for person in persons:
            p_answ = set([char for char in person])
            candidates.append(p_answ)
        common = set.intersection(*candidates)
        sum += len(common)
    return sum


if __name__ == '__main__':
    answers = load_input('./../data/6.txt')
    print(sum_groups(answers))
    print(sum_only_yes(answers))
