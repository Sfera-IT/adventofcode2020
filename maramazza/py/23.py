def getPuzzleInput():
    return [int(char) for char in "253149867"]


def solvePart1(cups):
    u = 0
    max_label = max(cups)

    for i in range(100):
        current = cups[u % 9]
        to_be_moved = [cups[(u+k+1) % 9] for k in range(3)]
        for each in to_be_moved:
            cups.remove(each)
        destination = current - 1
        if destination == 0:
            destination = max_label
        while destination not in cups or destination == current:
            destination -= 1
            if destination == 0:
                destination = max_label
        dest_index = cups.index(destination)
        cups.insert(dest_index + 1, to_be_moved[0])
        cups.insert(dest_index + 2, to_be_moved[1])
        cups.insert(dest_index + 3, to_be_moved[2])

        u = (cups.index(current) + 1) % 9
    return cups[(cups.index(1) + 1):] + cups[:cups.index(1)]


class Cup:
    def __init__(self, value):
        self.next = None
        self.value = value


def solvePart2(cups):
    total = 1000 * 1000
    moves = 10 * total
    lookup = {}
    prev = None
    for i in range(total):
        value = int(cups[i]) if i < len(cups) else i + 1
        cup = Cup(value)
        lookup[value] = cup
        if prev:
            prev.next = cup
        else:
            first = cup
        prev = cup
    prev.next = first
    current = first
    for x in range(moves):
        removed = current.next
        current.next = removed.next.next.next
        label = current.value
        while True:
            label -= 1
            if not label:
                label = total
            if label not in (removed.value, removed.next.value, removed.next.next.value):
                break
        dest = lookup[label]
        removed.next.next.next = dest.next
        dest.next = removed
        current = current.next

    one = lookup[1]

    return one.next.value * one.next.next.value


if __name__ == "__main__":
    puzzleInput = getPuzzleInput()
    answer1 = solvePart1(puzzleInput)
    answer1String = ''.join(str(e) for e in answer1)
    print(f"Res Part 1: {answer1String}")

    puzzleInput = getPuzzleInput()
    answer2 = solvePart2(puzzleInput)
    print(f"Res Part 2: {answer2}")
