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


def add_tile(a, b):
    def add_tuples(t1, t2):
        (a, b) = t1
        (c, d) = t2
        return a + c, b + d
    return add_tuples(a[0], b[0]), add_tuples(a[1], b[1])


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

    print(black_tiles)
    print("Num tiles", len(black_tiles))
