import numpy as np
from collections import defaultdict
import itertools

RIGHT, LEFT, DOWN, UP = 1, -1, 2, -2

# id -> direction -> id | None
direction_map = defaultdict(
    lambda: {LEFT: None, RIGHT: None, UP: None, DOWN: None}
)

matchers = {
    LEFT: lambda arr1, arr2: (arr2[:, -1] == arr1[:, 0]).all(),
    RIGHT: lambda arr1, arr2: (arr1[:, -1] == arr2[:, 0]).all(),
    UP: lambda arr1, arr2: (arr2[-1, :] == arr1[0, :]).all(),
    DOWN: lambda arr1, arr2: (arr1[-1, :] == arr2[0, :]).all()
}


def parse_tile(tile_sections):
    title, *data = tile_sections.splitlines()
    return (
        int(title.strip("Tile :")),
        np.array([list(line) for line in data])
    )


def get_tiles(file_string):
    return dict(map(parse_tile, file_string.split("\n\n")))


def transforms(arr):
    for (flip, rot) in itertools.product([True, False], [0, 1, 2, 3]):
        yield np.rot90(np.flip(arr, axis=1) if flip else arr, k=rot)


def get_adjacent_in_direction(tile, direction):
    for candidate in filter(lambda t: t is not tile and t not in locked_in, tiles):
        for transform in transforms(tiles_by_id.get(candidate)):
            if matchers.get(direction)(tiles_by_id.get(tile), transform):
                tiles_by_id[candidate] = transform
                return candidate


def trim_edges(grid):
    return np.array([
        [tiles_by_id.get(id)[1:-1, 1:-1] for id in row] for row in grid
    ])


def get_top_left():
    top_left = tiles[0]
    while (left := direction_map[top_left][LEFT]) is not None:
        top_left = left
    while (up := direction_map[top_left][UP]) is not None:
        top_left = up
    return top_left


def build_id_grid():
    start_of_line = get_top_left()
    image = []

    while True:  # Do while
        current_tile = start_of_line
        image.append([start_of_line])

        while True:  # Do while
            current_tile = direction_map[current_tile][RIGHT]
            image[-1].append(current_tile)
            if direction_map[current_tile][RIGHT] is None:
                break

        if direction_map[current_tile][DOWN] is None:
            break

        start_of_line = direction_map[start_of_line][DOWN]

    return np.array(image)


def get_full_image():
    frontier = {tiles[0]}

    while len(locked_in) < len(tiles):

        next_frontier = set()

        for frontier_tile in frontier:
            for direction in matchers.keys():
                if (adj := get_adjacent_in_direction(frontier_tile, direction)) is not None:
                    direction_map[frontier_tile][direction] = adj
                    direction_map[adj][-direction] = frontier_tile
                    next_frontier.add(adj)

        frontier = next_frontier
        locked_in.update(frontier)

    full_image = trim_edges(build_id_grid())

    return np.concatenate([np.concatenate(row, axis=1) for row in full_image], axis=0)


def get_sub_images(transformed, monster):
    image_height, image_width = transformed.shape
    monster_height, monster_width = monster.shape
    for dy in range(0, image_height - monster_height + 1):
        for dx in range(0, image_width - monster_width + 1):
            yield transformed[dy:dy + monster_height, dx:dx+monster_width]


def solve():

    monster = """
                  # 
#    ##    ##    ###
 #  #  #  #  #  #   
"""

    num_monster_squares = sum(x == "#" for x in monster)
    monster = np.array([
        list(line) for line in monster.splitlines() if line.strip(" ") != ""
    ])

    full_image = get_full_image()

    def is_sighting(sub_image):
        return len(monster[monster == sub_image]) == num_monster_squares

    for transformed in transforms(full_image):

        sightings = sum(map(
            is_sighting,
            get_sub_images(transformed, monster)
        ))

        if sightings > 1:
            break

    non_monster_squares = len(
        full_image[full_image == "#"]) - (sightings * num_monster_squares)
    print(non_monster_squares)


with open("inputs/day20.txt") as f:
    tiles_by_id = get_tiles(f.read())

    tiles = list(tiles_by_id.keys())
    locked_in = {tiles[0]}

    solve()
