def getPuzzleInput():
    puzzleInput = []
    with open("./../data/25.txt") as inputTxt:
        for line in inputTxt:
            puzzleInput.append(int(line.strip()))
    return puzzleInput


def solvePart1(subject_numbers):
    card = subject_numbers[0]
    door = subject_numbers[1]
    handshake = 1
    loopsize_card = 0
    loopsize_door = 0
    while handshake != card:
        loopsize_card += 1
        handshake *= 7
        handshake = handshake % 20201227

    handshake = 1
    while handshake != door:
        loopsize_door += 1
        handshake *= 7
        handshake = handshake % 20201227

    print("card: ", loopsize_card)
    print("door: ", loopsize_door)

    key = 1
    for i in range(loopsize_card):
        key *= door
        key = key % 20201227

    return key


def solvePart2(puzzleInput):
    pass


if __name__ == "__main__":
    puzzleInput = getPuzzleInput()

    answer1 = solvePart1(puzzleInput)
    print(f"Res Part 1: {answer1}")

    answer2 = solvePart2(puzzleInput)
    print(f"Res Part 2: {answer2}")
