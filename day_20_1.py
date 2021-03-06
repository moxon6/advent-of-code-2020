import numpy as np
from collections import namedtuple

Tile = namedtuple('Tile', ['id', 'data'])


def parse_tile_section(tile_sections):
    title, *data = tile_sections.splitlines()
    tile_id = int(title.strip("Tile :"))
    return Tile(
        id=tile_id,
        data=np.array([list(line) for line in data])
    )


def matches_right(arr1, arr2):
    return (arr1[:, -1] == arr2[:, 0]).all()


def matches_left(arr1, arr2):
    return matches_right(arr2, arr1)


def matches_down(arr1, arr2):
    return (arr1[-1, :] == arr2[0, :]).all()


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


with open("inputs/day20.txt") as f:
    tile_sections = f.read().split("\n\n")
    tiles = [parse_tile_section(section) for section in tile_sections]

    def get_adjacent_tiles(tile):

        adjacents = []

        for match_direction in [matches_left, matches_right, matches_up, matches_down]:
            def get_adjacent_in_direction():
                for candidate in tiles:
                    if (tile is candidate):
                        continue

                    for transform in transforms(candidate.data):
                        if match_direction(tile.data, transform):
                            return candidate
            adjacent = get_adjacent_in_direction()
            if adjacent is not None:
                adjacents.append(adjacent)
        return adjacents

    total = 1

    adjacents = {
        tile.id: get_adjacent_tiles(tile)
        for tile in tiles
    }

    total = np.prod([
        tile_id for tile_id, adjacent_tiles in adjacents.items() if len(adjacent_tiles) == 2
    ])

    print(total)
