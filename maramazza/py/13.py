def solPart1(timestamp, buses):
    waiting = 0
    while True:
        for buss in buses.values():
            if buss != 0:
                if (timestamp+waiting) % buss == 0:
                    return waiting * buss
        waiting += 1


def solPart2(buses):
    time = 0
    jump = buses[0]
    for timestamp, next_buss in buses.items():
        if next_buss == jump:
            continue
        tries = 0

        while (time + jump * tries + timestamp) % next_buss != 0:
            tries += 1

        time += tries * jump
        jump *= next_buss

    return time


def getPuzzleInput():
    timestamp = 0
    buses = {}
    i = 0
    with open("./../data/13.txt") as input_txt:
        for line in input_txt:
            if i == 0:
                timestamp = int(line.strip())
                i += 1
            else:
                for buss in line.strip().split(","):
                    if buss.isdigit():
                        buses[i-1] = int(buss)
                    i += 1
    return timestamp, buses


if __name__ == "__main__":
    timestamp, puzzleInput = getPuzzleInput()

    answer1 = solPart1(timestamp, puzzleInput)
    print(f"Res Part 1: {answer1}")

    answer2 = solPart2(puzzleInput)
    print(f"Res Part 2: {answer2}")
