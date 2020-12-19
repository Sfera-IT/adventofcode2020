import copy


def solvePart1(puzzleInput, passes):
    activeCubes = set()

    for x in range(len(puzzleInput)):
        for y in range(len(puzzleInput[0])):
            if puzzleInput[x][y] == '#':
                activeCubes.add((0, x, y))

    for _ in range(passes):
        minDimension = min(min(dimension for dimension in cube)
                           for cube in activeCubes)
        maxDimension = max(max(dimension for dimension in cube)
                           for cube in activeCubes)

        activeCubesNew = set()

        for z in range(minDimension - 1, maxDimension + 2):
            for x in range(minDimension - 1, maxDimension + 2):
                for y in range(minDimension - 1, maxDimension + 2):
                    count = 0

                    for zdiff in range(-1, 2):
                        for xdiff in range(-1, 2):
                            for ydiff in range(-1, 2):
                                if zdiff == 0 and xdiff == 0 and ydiff == 0:
                                    continue

                                if (z + zdiff, x + xdiff, y + ydiff) in activeCubes:
                                    count += 1

                    if count == 3 or (count == 2 and (z, x, y) in activeCubes):
                        activeCubesNew.add((z, x, y))

        activeCubes = activeCubesNew

    return len(activeCubes)


def solvePart2(puzzleInput, passes):
    activeCubes = set()

    for x in range(len(puzzleInput)):
        for y in range(len(puzzleInput[0])):
            if puzzleInput[x][y] == '#':
                activeCubes.add((0, 0, x, y))

    for _ in range(passes):
        minDimension = min(min(dimension for dimension in cube)
                           for cube in activeCubes)
        maxDimension = max(max(dimension for dimension in cube)
                           for cube in activeCubes)

        activeCubesNew = set()
        for w in range(minDimension-1, maxDimension + 2):
            for z in range(minDimension - 1, maxDimension + 2):
                for x in range(minDimension - 1, maxDimension + 2):
                    for y in range(minDimension - 1, maxDimension + 2):
                        count = 0

                        for wdiff in range(-1, 2):
                            for zdiff in range(-1, 2):
                                for xdiff in range(-1, 2):
                                    for ydiff in range(-1, 2):
                                        if wdiff == 0 and zdiff == 0 and xdiff == 0 and ydiff == 0:
                                            continue

                                        if (w + wdiff, z + zdiff, x + xdiff, y + ydiff) in activeCubes:
                                            count += 1

                        if count == 3 or (count == 2 and (w, z, x, y) in activeCubes):
                            activeCubesNew.add((w, z, x, y))

        activeCubes = activeCubesNew

    return len(activeCubes)


def getPuzzleInput():
    puzzleInput = []
    with open("./../data/17.txt") as inputTxt:
        for line in inputTxt:
            puzzleInput.append(line.strip())
    return puzzleInput


if __name__ == "__main__":
    puzzleInput = getPuzzleInput()

    answer1 = solvePart1(puzzleInput, 6)
    print(f"Res Part 1: {answer1}")

    answer2 = solvePart2(puzzleInput, 6)
    print(f"Part 2: {answer2}")
