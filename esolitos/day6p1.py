from collections.abc import Iterable

test_data = "abc abc abac aaaa b"


def unique_answers_count(answers: str) -> int:
    return len(set(answers))


def unique_answer_total(groups: Iterable) -> int:
    totals = 0
    for item in groups:
        totals += unique_answers_count(item.strip())

    return totals


if __name__ == '__main__':
    print("Test data: " + str(unique_answer_total(test_data.split(' '))))

    data = open('./input/6.txt').read().replace('\n\n', '|').replace('\n', '').split('|')
    print("Sum: " + str(unique_answer_total(data)))
