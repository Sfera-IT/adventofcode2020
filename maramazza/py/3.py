def contaAlberi(map, right, down):
    totCount = 0
    for i, row in enumerate(map):
        if i == 0:
            # salta prima riga
            pass
        else:
            # ricordati di ignorare la prima riga
            if ((1 + i) % down) == 0:
                if row[(i * right) % len(row)] == 1:
                    totCount += 1
    return totCount


if __name__ == "__main__":
    map = []

    with open('./../data/3.txt', 'r') as f:
        for line in f:
            row = []
            for element in line:
                if element == '.':  # no tree
                    row.append(0)
                elif element == '#':  # tree
                    row.append(1)
                else:
                    pass
            map.append(row)

    # part 1
    print(f'Result Part 1: {contaAlberi(map, 3, 1)}')

    # part 2
    res = 1
    res *= contaAlberi(map, 1, 1)
    res *= contaAlberi(map, 3, 1)
    res *= contaAlberi(map, 5, 1)
    res *= contaAlberi(map, 7, 1)
    res *= contaAlberi(map, 1, 2)
    print(f'Result Part 2: {res}')
