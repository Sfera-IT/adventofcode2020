data = {}

with open("./../data/11.txt") as f:
    y = 0
    for _y in [line.rstrip() for line in f]:
        x = 0
        for _x in _y:
            data[(y, x)] = _x
            x += 1
        y += 1
directions = [(-1, -1), (-1, 0), (1, 0), (1, -1), (0, -1), (0, 1), (1, 1), (-1, 1)]


def adjacentOccupied(point, grid):
    adjacentPoints = [(point[0] + y, point[1] + x) for y, x in directions]
    return len([p for p in adjacentPoints if grid.get(p, '.') == '#'])


def solPart1(g):
    grid = dict(g)
    old_grid = dict()
    while grid != old_grid:
        adjacent = {k: adjacentOccupied(k, grid) for k in grid.keys()}
        old_grid = grid.copy()
        for point in grid.keys():
            if grid[point] == '#' and adjacent[point] >= 4:
                grid[point] = 'L'
            elif grid[point] == 'L' and adjacent[point] == 0:
                grid[point] = '#'
    return sum(value == "#" for value in grid.values())


print(solPart1(data))


def visibleOccupied(point, grid):
    visible = 0
    for y, x in directions:
        dy, dx = point[0] + y, point[1] + x
        while (dy, dx) in grid.keys():
            if grid[(dy, dx)] != '.':
                visible += 1 if grid[(dy, dx)] == '#' else 0
                break
            dy += y
            dx += x
    return visible


def solPart2(g):
    grid = dict(g)
    old_grid = dict()
    while grid != old_grid:
        visible = {k: visibleOccupied(k, grid) for k in grid.keys()}
        old_grid = grid.copy()
        for point in grid.keys():
            if grid[point] == '#' and visible[point] >= 5:
                grid[point] = 'L'
            elif grid[point] == 'L' and visible[point] == 0:
                grid[point] = '#'
    return sum(value == '#' for value in grid.values())


print(solPart2(data))
