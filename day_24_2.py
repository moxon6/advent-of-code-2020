from functools import reduce


def parse_line(line):
    line = list(line.strip(" \n"))
    for i, x in enumerate(line):
        if x == "s" or x == "n":
            line[i], line[i+1] = line[i] + line[i+1], None
    return [x for x in line if x is not None]


ref = ((0, 0), (0, 0))

# Assume side length 2: (a,b) <-> a + b * sqrt(3)
directions_map = {
    "w": ((0, -2), (0, 0)),
    "e": ((0, 2), (0, 0)),
    "ne": ((0, 1), (1, 1)),
    "nw": ((0, -1), (1, 1)),
    "se": ((0, 1), (-1, -1)),
    "sw": ((0, -1), (-1, -1))
}


def add_tuples(t1, t2):
    (a, b) = t1
    (c, d) = t2
    return a + c, b + d


def add_tile(a, b):
    return add_tuples(a[0], b[0]), add_tuples(a[1], b[1])


def get_adjacents(tile):
    return [add_tile(tile, x) for x in directions_map.values()]


with open("inputs/day24.txt") as f:
    lines = f.readlines()
    tiles = [parse_line(line) for line in lines]

    black_tiles = set()

    for tile in tiles:
        directions = map(directions_map.get, tile)

        destination = reduce(add_tile, directions, ref)
        if destination in black_tiles:
            black_tiles.remove(destination)
        else:
            black_tiles.add(destination)


def count_adjacent_black_tiles(black_tiles, tile):
    return sum(tile in black_tiles for tile in get_adjacents(tile))


for day in range(100):
    white_tiles = {
        tile for x in map(get_adjacents, black_tiles)
        for tile in x
        if tile not in black_tiles
    }

    tiles_to_toggle = set()

    for tile in black_tiles:
        if count_adjacent_black_tiles(black_tiles, tile) not in [1, 2]:
            tiles_to_toggle.add(tile)
    for tile in white_tiles:
        if count_adjacent_black_tiles(black_tiles, tile) == 2:
            tiles_to_toggle.add(tile)
    for tile in tiles_to_toggle:
        if tile not in black_tiles:
            black_tiles.add(tile)
        else:
            black_tiles.remove(tile)
    print("Day", day + 1, "black tiles:", len(black_tiles))
