def tranToBinary(string):
    string = string.replace('L', '0')
    string = string.replace('R', '1')
    string = string.replace('F', '0')
    string = string.replace('B', '1')

    return int(string, 2)


if __name__ == "__main__":
    data = []

    with open('./../data/5.txt') as f:
        for line in f:
            data.append(line.strip())

    # part 1
    dataBin = []
    for seat in data:
        dataBin.append(tranToBinary(seat))

    print(f'Result Part 1: {max(dataBin)}')

    # part 2
    for i in range(1024):
        if i not in dataBin:
            if i + 1 in dataBin and i - 1 in dataBin:
                print(f'Result Part 2: {i}')
