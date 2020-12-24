from collections import defaultdict, Counter


def getPuzzleInput():
    instructions = defaultdict(list)
    j = 0
    with open("./../data/24.txt") as input_txt:
        for line in input_txt:
            i = 0
            while i < len(line.strip()):
                if line[i] == "e" or line[i] == "w":
                    instructions[j].append(line[i])
                    i += 1
                else:
                    instructions[j].append(line[i] + line[i + 1])
                    i += 2
            j += 1
    return instructions


def solvePart1(instructions):
    black = set()

    for line in instructions:
        x, y = 0, 0
        for instruction in instructions[line]:
            if instruction == "e":
                x += 1
            if instruction == "w":
                x -= 1
            if instruction == "se":
                y += 1
            if instruction == "sw":
                x -= 1
                y += 1
            if instruction == "ne":
                x += 1
                y -= 1
            if instruction == "nw":
                y -= 1

        if (x, y) in black:
            black.remove((x, y))
        else:
            black.add((x, y))

    return black, len(black)


COORDS = {
    'e': (1, 0),
    'se': (0, 1),
    'sw': (-1, 1),
    'w': (-1, 0),
    'ne': (1, -1),
    'nw': (0, -1)
}


def solvePart2(black):
    for _ in range(100):
        # Track adjacent 'live' counts, also serves as a bounds-checking mechanic
        adjacent = Counter()
        next_black = set()  # Next state
        for x, y in black:
            for dx, dy in COORDS.values():
                adjacent[x + dx, y + dy] += 1

        for coords, count in adjacent.items():
            if count == 2 or (coords in black and count == 1):
                next_black.add(coords)

        black = next_black

    return len(black)


if __name__ == "__main__":
    puzzleInput = getPuzzleInput()

    black, answer1 = solvePart1(puzzleInput)
    print(f"Res Part 1: {answer1}")

    answer2 = solvePart2(black)
    print(f"Res Part 2: {answer2}")

