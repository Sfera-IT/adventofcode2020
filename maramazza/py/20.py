import collections
import itertools

inp = open('./../data/20.txt').read()

tiles_lines = inp.strip().split('\n\n')

tiles_sides = {}
tiles = {}
for tile_lines in tiles_lines:
    name, lines = tile_lines[5:].split(':\n')
    lines = lines.split()
    rt, lt = '', ''
    for line in lines:
        rt += line[-1]
        lt += line[0]

    tiles_sides[name] = (lines[0], rt, lines[-1], lt)
    tiles[name] = lines


def to_num(s):
    return int(s.replace('#', '1').replace('.', '0'), 2)


tiles_num = {}
for name, strs in tiles_sides.items():
    tiles_num[name] = tuple(map(to_num, strs))


def reverse_side(side):
    return int(''.join(reversed(format(side, '010b'))), 2)


def find_adjacent(base_name):
    base_possible_sides = set()
    base_possible_sides.update(tiles_num[base_name])
    base_possible_sides.update(map(reverse_side, tiles_num[base_name]))
    possible_adjacent = set()
    for name, sides in tiles_num.items():
        if name == base_name:
            continue
        possible_sides = set()
        possible_sides.update(sides)
        possible_sides.update(map(reverse_side, sides))
        if len(base_possible_sides.intersection(possible_sides)):
            possible_adjacent.add(name)
    return possible_adjacent


adjacent = {}
for name, sides in tiles_num.items():
    adjacent[name] = find_adjacent(name)

corners = set()
sides = set()
for name in sorted(adjacent.keys()):
    num_adj = len(adjacent[name])
    if num_adj == 2:
        corners.add(name)
    elif num_adj == 3:
        sides.add(name)

prod = 1
for name in corners:
    prod *= int(name)
print('part1:', prod)


def find_side(side_name, opposite_name):
    sides = list(adjacent[side_name] - {opposite_name})
    # print('fs', sides)
    if len(adjacent[sides[0]]) != 4:
        return sides[0]
    else:
        return sides[1]


image = []
row = []
cur = list(corners)[0]  # This will be the top left corner.
while True:
    row.append(cur)
    adj = adjacent[cur]
    if len(adj) == 2 and len(row) == 1:
        nxt = list(adj)[0]
        cur = nxt
    elif len(adj) == 2 and len(row) > 1:
        break
    else:
        cur = find_side(cur, row[-2])
image.append(row)

# Build the left side of the image.
side_len = len(sides) // 4 + 2
cur = list(adjacent[row[0]] - {row[1]})[0]
while True:
    image.append([cur])
    if len(adjacent[cur]) == 2:
        break
    cur = find_side(cur, image[-2][0])

# Now fill in the image.
for r in range(1, side_len):
    for c in range(1, side_len):
        p = list(
            adjacent[image[r][c-1]].intersection(adjacent[image[r-1][c]]) - {image[r-1][c-1]})
        if len(p) != 1:
            raise Exception('%d %d %s' % (r, c, p))
        image[r].append(p[0])


def rotate_cw(tile):
    new_tile = []
    for c in range(len(tile[0])):
        row = ''
        for r in range(len(tile) - 1, -1, -1):
            row += tile[r][c]
        new_tile.append(row)
    return new_tile


def flip(tile):
    new_tile = []
    for row in tile:
        new_tile.append(''.join(reversed(row)))
    return new_tile


def gen_permutations(tile):
    for i in range(4):
        yield tile
        tile = rotate_cw(tile)
    tile = flip(tile)
    for i in range(4):
        yield tile
        tile = rotate_cw(tile)


TOP, RT, BOT, LT = range(4)


def get_side(tile, side):
    if side == TOP:
        return tile[0]
    elif side == BOT:
        return tile[-1]
    elif side == RT:
        return ''.join(r[-1] for r in tile)
    else:
        return ''.join(r[0] for r in tile)


images_positioned = []
for corner, bottom in itertools.product(
        gen_permutations(tiles[image[0][0]]),
        gen_permutations(tiles[image[1][0]])):
    if get_side(corner, BOT) == get_side(bottom, TOP):
        break

match = False
for right in gen_permutations(tiles[image[0][1]]):
    if get_side(corner, RT) == get_side(right, LT):
        match = True
        break
if not match:
    corner = flip(corner)
    bottom = flip(bottom)
    assert get_side(corner, BOT) == get_side(bottom, TOP)
    for right in gen_permutations(tiles[image[0][1]]):
        if get_side(corner, RT) == get_side(right, LT):
            match = True
            break
assert match

# for r1, r2 in zip(corner, right):
#   print(r1, r2)
# for row in bottom:
#   print(row)

tiles[image[0][0]] = corner
tiles[image[0][1]] = right
tiles[image[1][0]] = bottom

# Fill in the left side.
for r in range(2, side_len):
    top = tiles[image[r-1][0]]
    for bottom in gen_permutations(tiles[image[r][0]]):
        if get_side(top, BOT) == get_side(bottom, TOP):
            tiles[image[r][0]] = bottom

# For the remaining tiles, there should be only one valid orientation.
for r in range(side_len):
    for c in range(1, side_len):
        left = tiles[image[r][c-1]]
        for right in gen_permutations(tiles[image[r][c]]):
            if get_side(left, RT) == get_side(right, LT):
                tiles[image[r][c]] = right
                break

# The image itself doesn't include the border of each tile.
full_image = []
for r in range(side_len):
    for l in range(1, 9):
        full_image.append(''.join(tiles[tile_num][l][1:-1]
                                  for tile_num in image[r]))

# Count sea monsters (we rotate the monster instead of the image).
MONSTER = ['                  # ',  # Text editor was eating the trailing space.
           '#    ##    ##    ###',
           ' #  #  #  #  #  #   ']


def has_monster(monster, r, c):
    for mr, mrow in enumerate(monster):
        for mc, ch in enumerate(mrow):
            if ch == '#':
                if full_image[r+mr][c+mc] != '#':
                    return False
    return True


for monster in gen_permutations(MONSTER):
    cnt = 0
    for r in range(len(full_image) - len(monster) + 1):
        for c in range(len(full_image[0]) - len(monster[0]) + 1):
            if has_monster(monster, r, c):
                cnt += 1
    if cnt != 0:
        total_pounds = sum(row.count('#') for row in full_image)
        monster_pounds = sum(row.count('#') for row in monster)
        print('part2:', total_pounds - (monster_pounds * cnt))
        break
