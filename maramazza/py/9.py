def anyequalto(x, y):
    for i in x:
        if y - i in x:
            return True

if __name__ == "__main__":
    data = []

    with open('./../data/9.txt','r') as f:
        data = f.read()[:-1].split('\n')

    numbers = list(map(int, data))

    # part 1
    for i, number in enumerate(numbers):
        if i >= 25:
            if not anyequalto(numbers[i-25:i], number):
                print(f'Res Part1: {number}')
                break

    # part 2
    for i in range(len(numbers)):
        if not numbers[i] == number:
            for j in range(len(numbers)-i):
                seg = numbers[i:i+j]
                if sum(seg) == number:
                    print(f'Res Part2: {min(seg) + max(seg)}')