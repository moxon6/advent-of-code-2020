import numpy as np
from recordclass import recordclass

Tile = recordclass('Tile', ['id', 'data'])

def parse_tile_section(tile_sections):
    title, *data = tile_sections.splitlines()
    tile_id = int( title.strip("Tile :") )
    return Tile(
        id = tile_id,
        data = np.array([list(line) for line in data])
    )

def matches_right(arr1, arr2):
    return (arr1[:,-1] == arr2[:,0]).all()

def matches_left(arr1, arr2):
    return matches_right(arr2, arr1)

def matches_down(arr1, arr2):
    return (arr1[-1,:] == arr2[0,:]).all()

def matches_up(arr1, arr2):
    return matches_down(arr2, arr1)

def make_transform(flip, rot):
    def op(arr):
        if flip:
            arr = np.flip(arr, axis=1)
        return np.rot90(arr, k=rot)
    return op

def transforms(arr):
    for flip in [True, False]:
        for rot in [0, 1, 2, 3]:
            yield make_transform(flip, rot)(arr)

def get_adjacent_in_direction(tile, match_direction):
    for candidate in tiles:
        if (tile is candidate):
            continue

        for transform in transforms(candidate.data):
            if match_direction(tile.data, transform):
                candidate.data = transform
                return candidate

with open("inputs/day20.txt") as f:
    tile_sections = f.read().split("\n\n")
    tiles = [ parse_tile_section(section) for section in tile_sections ]

    def invert_cache(cache):
        if cache == get_left:
            return get_right
        if cache == get_right:
            return get_left
        if cache == get_above:
            return get_below
        if cache == get_below:
            return get_above

    match_directions = [matches_left, matches_right, matches_up, matches_down]

    def get_adjacent_tiles(tile):
        adjacents = [ get_adjacent_in_direction(tile, direction) for direction in match_directions ]
        return [x for x in adjacents if x is not None]

    adjacents = {
        tile.id : get_adjacent_tiles(tile)
        for tile in tiles
    }

    total = np.prod([
        tile_id for tile_id, adjacent_tiles in adjacents.items() if len(adjacent_tiles) == 2
    ])

    print(total)