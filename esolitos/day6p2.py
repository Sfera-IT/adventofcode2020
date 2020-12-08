from collections.abc import Iterable

test_data = "abc|a.b.c|ab.ac|a.a.a.a|b"


def all_yes_count(answers_set: list) -> int:
    final_set = set(answers_set[0])
    for answers in answers_set[1:]:
        final_set = final_set & set(answers)

    return len(final_set)


def all_yes_totals(groups: Iterable) -> int:
    totals = 0
    for item in groups:
        totals += all_yes_count(item.split('\n'))

    return totals


if __name__ == '__main__':
    all_groups = test_data.replace('.', '\n').split('|')
    all_yes = all_yes_totals(all_groups)
    print(f"Test: {all_yes}")

    data = open('./input/6.txt').read().strip().split('\n\n')
    all_yes = all_yes_totals(data)
    print(f"Sum: {all_yes}")
