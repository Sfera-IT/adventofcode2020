from lark import Lark

raw_rules, data = open("./../data/19.txt").read().split("\n\n")
data = data.splitlines()


def solvePart1(data):
    parser = Lark(
        "start: j\n"
        + raw_rules.replace("1", "a")
        .replace("2", "b")
        .replace("3", "c")
        .replace("4", "d")
        .replace("5", "e")
        .replace("6", "f")
        .replace("7", "g")
        .replace("8", "h")
        .replace("9", "i")
        .replace("0", "j")
    )

    total = 0
    for item in data:
        try:
            parser.parse(item)
            total += 1
        except Exception as e:
            pass

    return total


def solvePart2(data):
    parser = Lark(
        "start: j\n"
        + raw_rules.replace("8: 42", "8: 42 | 42 8")
        .replace("11: 42 31", "11: 42 31 | 42 11 31")
        .replace("1", "a")
        .replace("2", "b")
        .replace("3", "c")
        .replace("4", "d")
        .replace("5", "e")
        .replace("6", "f")
        .replace("7", "g")
        .replace("8", "h")
        .replace("9", "i")
        .replace("0", "j")
    )

    total = 0
    for item in data:
        try:
            parser.parse(item)
            total += 1
        except Exception as e:
            pass

    return total


print(f"Res Part 1: {solvePart1(data)}")
print(f"Res Part 2: {solvePart2(data)}")
