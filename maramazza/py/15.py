def solvePart1(puzzle_input, limit):
    spoken_numbers = {}
    numbers = puzzle_input.split(",")
    for index, number in enumerate(numbers):
        spoken_numbers[int(number)] = [index+1]
    last_number_spoken = numbers[-1]
    i = len(numbers) + 1
    while i <= limit:
        if last_number_spoken in spoken_numbers.keys() and len(spoken_numbers[last_number_spoken]) > 1:
            first_appearance = spoken_numbers[last_number_spoken][-2]
            last_number_spoken = i-1 - first_appearance
            if last_number_spoken in spoken_numbers.keys():
                spoken_numbers[last_number_spoken].append(i)
            else:
                spoken_numbers[last_number_spoken] = [i]
        else:
            last_number_spoken = 0
            spoken_numbers[last_number_spoken].append(i)
        i += 1
    return last_number_spoken


def solvePart2(puzzle_input, limit):
    return solvePart1(puzzle_input, limit)


def getPuzzleInput():
    puzzleInput = []
    with open("./../data/15.txt") as inputTxt:
        for line in inputTxt:
            puzzleInput = line.strip()
    return puzzleInput


if __name__ == "__main__":
    puzzleInput = getPuzzleInput()

    answer1 = solvePart1(puzzleInput, 2020)
    print(f"Res Part 1: {answer1}")

    answer2 = solvePart2(puzzleInput, 30000000)
    print(f"Res Part 2: {answer2}")
