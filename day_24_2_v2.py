from functools import reduce


def parse_line(line):
    line = list(line.strip(" \n"))
    for i, x in enumerate(line):
        if x == "s" or x == "n":
            line[i], line[i+1] = line[i] + line[i+1], None
    return [x for x in line if x is not None]


# Same as previous day_24_2.py but factor out (0,1) from x and (1,1) from y coordinates
directions_map = {
    "w": (-2, 0),
    "e": (2, 0),
    "ne": (1, 1),
    "nw": (-1, 1),
    "se": (1,  -1),
    "sw": (-1, -1)
}


def add_tile(a, b):
    return a[0] + b[0], a[1] + b[1]


def get_adjacents(tile):
    return [add_tile(tile, x) for x in directions_map.values()]


with open("inputs/day24.txt") as f:
    black_tiles = set()
    for tile in map(parse_line, f.readlines()):
        directions = map(directions_map.get, tile)
        destination = reduce(add_tile, directions, (0, 0))
        black_tiles ^= {destination}


def count_adjacent_black_tiles(tile):
    return sum(tile in black_tiles for tile in get_adjacents(tile))


for day in range(100):
    white_tiles = {
        tile for x in map(get_adjacents, black_tiles)
        for tile in x
        if tile not in black_tiles
    }

    black_tiles ^= {
        *filter(lambda tile: count_adjacent_black_tiles(tile) not in [1, 2], black_tiles),
        *filter(lambda tile: count_adjacent_black_tiles(tile) == 2, white_tiles)
    }
    print("Day", day + 1, "black tiles:", len(black_tiles))
