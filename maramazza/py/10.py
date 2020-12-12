from collections import Counter, defaultdict

# part 1
def find_differences(data):
    diff = Counter()
    for i, adapter in enumerate(data):
        if i != 0:
            diff[adapter - data[i-1]] += 1

    return diff[1]*diff[3]

# part 2
def find_distinct_ways(i, data):
    ways = defaultdict(int)
    ways[0] = 1
    for i, adapter in enumerate(data):
        if i != 0:
            ways[adapter] = ways[adapter - 1] + \
                ways[adapter - 2] + ways[adapter - 3]
    return ways[data[-1]]


if __name__ == "__main__":
    data = []

    with open('./../data/10.txt', 'r') as f:
        data = list(map(int, f.read().splitlines()))
    data += [0, max(data) + 3]
    data.sort()

    print(f'Res Part 1:{find_differences(data)}')
    print(f'Res Part2: {find_distinct_ways(1, data.copy())}')
