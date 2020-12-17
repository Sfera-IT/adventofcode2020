import copy


def energy_cycle(grid, new_grid):
    pass


def solve_part_1(puzzle_input, passes):
    active_cubes = set()

    for x in range(len(puzzle_input)):
        for y in range(len(puzzle_input[0])):
            if puzzle_input[x][y] == '#':
                active_cubes.add((0, x, y))

    for _ in range(passes):
        min_dimension = min(min(dimension for dimension in cube)
                            for cube in active_cubes)
        max_dimension = max(max(dimension for dimension in cube)
                            for cube in active_cubes)

        active_cubes_new = set()

        for z in range(min_dimension - 1, max_dimension + 2):
            for x in range(min_dimension - 1, max_dimension + 2):
                for y in range(min_dimension - 1, max_dimension + 2):
                    count = 0

                    for zdiff in range(-1, 2):
                        for xdiff in range(-1, 2):
                            for ydiff in range(-1, 2):
                                if zdiff == 0 and xdiff == 0 and ydiff == 0:
                                    continue

                                if (z + zdiff, x + xdiff, y + ydiff) in active_cubes:
                                    count += 1

                    if count == 3 or (count == 2 and (z, x, y) in active_cubes):
                        active_cubes_new.add((z, x, y))

        active_cubes = active_cubes_new

    return len(active_cubes)


def solve_part_2(puzzle_input, passes):
    active_cubes = set()

    for x in range(len(puzzle_input)):
        for y in range(len(puzzle_input[0])):
            if puzzle_input[x][y] == '#':
                active_cubes.add((0, 0, x, y))

    for _ in range(passes):
        min_dimension = min(min(dimension for dimension in cube)
                            for cube in active_cubes)
        max_dimension = max(max(dimension for dimension in cube)
                            for cube in active_cubes)

        active_cubes_new = set()
        for w in range(min_dimension-1, max_dimension + 2):
            for z in range(min_dimension - 1, max_dimension + 2):
                for x in range(min_dimension - 1, max_dimension + 2):
                    for y in range(min_dimension - 1, max_dimension + 2):
                        count = 0

                        for wdiff in range(-1, 2):
                            for zdiff in range(-1, 2):
                                for xdiff in range(-1, 2):
                                    for ydiff in range(-1, 2):
                                        if wdiff == 0 and zdiff == 0 and xdiff == 0 and ydiff == 0:
                                            continue

                                        if (w + wdiff, z + zdiff, x + xdiff, y + ydiff) in active_cubes:
                                            count += 1

                        if count == 3 or (count == 2 and (w, z, x, y) in active_cubes):
                            active_cubes_new.add((w, z, x, y))

        active_cubes = active_cubes_new

    return len(active_cubes)


def get_puzzle_input():
    puzzle_input = []
    with open("./../data/17.txt") as input_txt:
        for line in input_txt:
            puzzle_input.append(line.strip())
    return puzzle_input


if __name__ == "__main__":
    puzzle_input = get_puzzle_input()

    answer_1 = solve_part_1(puzzle_input, 6)
    print(f"Res Part 1: {answer_1}")

    answer_2 = solve_part_2(puzzle_input, 6)
    print(f"Part 2: {answer_2}")
