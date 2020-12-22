from collections import deque
from functools import reduce


def evaluate_simple(line):
    while '+' in line:
        add_index = -1

        for index, char in enumerate(line):
            if char == '+':
                add_index = index
                break

        line = line[:add_index - 1] + [line[add_index - 1] +
                                       line[add_index + 1]] + line[add_index + 2:]

    return reduce(lambda a, b: a * b, [num for num in line if isinstance(num, int)])


def evaluate_line(line):
    list_line = list(line)

    for x in range(len(list_line)):
        if list_line[x].isdigit():
            list_line[x] = int(list_line[x])

    while True:
        parentheses = []
        stack = []

        for index, char in enumerate(list_line):
            if char == '(':
                stack.append(index)
            elif char == ')':
                parentheses.append((stack.pop(), index))

        open_index = -1
        close_index = -1

        for open, close in parentheses:
            if not any(paren[0] > open and paren[1] < close for paren in parentheses):
                open_index = open
                close_index = close
                break

        if open_index == -1:
            break

        list_line = list_line[:open_index] + [evaluate_simple(
            list_line[open_index + 1:close_index])] + list_line[close_index + 1:]

    return evaluate_simple(list_line)


def solvePart1(puzzle_input):
    result = 0
    for line in puzzle_input:
        num = 0
        add = True
        stack = deque()
        for char in line:
            if char == "(":
                stack.append((num, add))
                add = True
                num = 0
            elif char == ")":
                (number, is_add) = stack.pop()
                if is_add:
                    num += number
                else:
                    num *= number
            elif char == "+":
                add = True
            elif char == "*":
                add = False
            else:
                number = int(char)
                if add:
                    num += number
                else:
                    num *= number
        result += num
    return result


def solvePart2(puzzle_input):
    return sum(map(evaluate_line, puzzle_input))


def getPuzzleInput():
    puzzle_input = []
    with open("./../data/18.txt") as input_txt:
        for line in input_txt:
            puzzle_input.append(line.strip().replace(" ", ""))
    return puzzle_input


if __name__ == "__main__":
    puzzleInput = getPuzzleInput()

    answer1 = solvePart1(puzzleInput)
    print(f"Res Part 1: {answer1}")

    answer2 = solvePart1(puzzleInput)
    print(f"Res Part 2: {answer2}")
