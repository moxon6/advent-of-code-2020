import numpy as np
import itertools

RIGHT, LEFT, DOWN, UP = 1, 2, 3, 4
matchers = {
    LEFT: lambda arr1, arr2: (arr2[:, -1] == arr1[:, 0]).all(),
    RIGHT: lambda arr1, arr2: (arr1[:, -1] == arr2[:, 0]).all(),
    UP: lambda arr1, arr2: (arr2[-1, :] == arr1[0, :]).all(),
    DOWN: lambda arr1, arr2: (arr1[-1, :] == arr2[0, :]).all()
}
monster_string = """
                  # 
#    ##    ##    ###
 #  #  #  #  #  #   
"""


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
    for candidate in filter(lambda t: t is not tile, tiles):
        for transform in transforms(tiles_by_id.get(candidate)):
            if matchers.get(direction)(tiles_by_id.get(tile), transform):
                tiles_by_id[candidate] = transform
                return candidate


def trim_edges(grid):
    return np.array([
        [tiles_by_id.get(id)[1:-1, 1:-1] for id in row] for row in grid
    ])


def get_top_left():
    position = tiles[0]
    while (left := get_adjacent_in_direction(position, LEFT)) is not None:
        position = left
    while (up := get_adjacent_in_direction(position, UP)) is not None:
        position = up
    return position


def build_id_grid():
    id_grid = []
    start_of_line = get_top_left()
    while start_of_line is not None:
        id_grid.append([])
        current_tile = start_of_line
        while current_tile is not None:
            id_grid[-1].append(current_tile)
            current_tile = get_adjacent_in_direction(current_tile, RIGHT)
        start_of_line = get_adjacent_in_direction(start_of_line, DOWN)
    return np.array(id_grid)


def get_full_image():
    full_image = trim_edges(build_id_grid())
    return np.concatenate([np.concatenate(row, axis=1) for row in full_image], axis=0)


def get_sub_images(image, monster):
    image_height, image_width = image.shape
    monster_height, monster_width = monster.shape

    for (dx, dy) in itertools.product(range(image_width - monster_width + 1), range(image_height - monster_height + 1)):
        yield image[dy:dy + monster_height, dx:dx+monster_width]


def solve():
    num_monster_squares = sum(x == "#" for x in monster_string)
    monster = np.array([
        list(line) for line in monster_string.splitlines() if line.strip(" ") != ""
    ])

    def is_sighting(sub_image):
        return len(monster[monster == sub_image]) == num_monster_squares
    full_image = get_full_image()
    for transformed in transforms(full_image):
        sightings = sum(map(
            is_sighting,
            get_sub_images(transformed, monster)
        ))
        if sightings > 1:
            non_monster_squares = len(
                full_image[full_image == "#"]) - (sightings * num_monster_squares)
            print(non_monster_squares)


with open("inputs/day20.txt") as f:
    tiles_by_id = get_tiles(f.read())
    tiles = list(tiles_by_id.keys())
    solve()
