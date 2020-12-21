import numpy as np
from collections import defaultdict

RIGHT, LEFT, DOWN, UP = 1, -1, 2, -2

# id -> direction -> id | None
direction_map = defaultdict(
    lambda: {LEFT: None, RIGHT: None, UP: None, DOWN: None}
)


def parse_tile(tile_sections):
    title, *data = tile_sections.splitlines()
    return (
        int(title.strip("Tile :")),
        np.array([list(line) for line in data])
    )


def get_tiles(file_string):
    return dict(map(
        parse_tile,
        file_string.split("\n\n")
    ))


get_matcher = {
    LEFT: lambda arr1, arr2: (arr2[:, -1] == arr1[:, 0]).all(),
    RIGHT: lambda arr1, arr2: (arr1[:, -1] == arr2[:, 0]).all(),
    UP: lambda arr1, arr2: (arr2[-1, :] == arr1[0, :]).all(),
    DOWN: lambda arr1, arr2: (arr1[-1, :] == arr2[0, :]).all()
}


def do_transform(arr, flip, rot):
    if flip:
        arr = np.flip(arr, axis=1)
    return np.rot90(arr, k=rot)


def transforms(arr):
    for flip in [True, False]:
        for rot in [0, 1, 2, 3]:
            yield do_transform(arr, flip, rot)


def get_adjacent_in_direction(tile, direction):
    for candidate in filter(lambda t: t is not tile and t not in locked_in, tiles):
        for transform in transforms(gtd(candidate)):
            if get_matcher[direction](gtd(tile), transform):
                tiles_by_id[candidate] = transform
                return candidate


def get_and_transform_adjacent_tiles(tile):
    return [get_adjacent_in_direction(tile, direction) for direction in [LEFT, RIGHT, UP, DOWN]]


def trim_edges(arr):
    return arr[1:-1, 1:-1]


def get_id_grid(top_left):
    start_of_line = top_left
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
    frontier = [tiles[0]]

    while len(locked_in) < len(tiles):

        new_frontier = set()

        for frontier_tile in frontier:
            (left, right, up, down) = get_and_transform_adjacent_tiles(
                frontier_tile)
            if left is not None and left not in locked_in:
                direction_map[frontier_tile][LEFT] = left
                direction_map[left][RIGHT] = frontier_tile
                new_frontier.add(left)
            if right is not None and right not in locked_in:
                direction_map[frontier_tile][RIGHT] = right
                direction_map[right][LEFT] = frontier_tile
                new_frontier.add(right)
            if up is not None and up not in locked_in:
                direction_map[frontier_tile][UP] = up
                direction_map[up][DOWN] = frontier_tile
                new_frontier.add(up)
            if down is not None and down not in locked_in:
                direction_map[frontier_tile][DOWN] = down
                direction_map[down][UP] = frontier_tile
                new_frontier.add(down)

        frontier = new_frontier
        locked_in.update(frontier)

    top_left = tiles[0]
    while direction_map[top_left][LEFT] is not None:
        top_left = direction_map[top_left][LEFT]
    while direction_map[top_left][UP] is not None:
        top_left = direction_map[top_left][UP]

    image = get_id_grid(top_left)

    full_image = np.array([
        [trim_edges(gtd(id)) for id in row] for row in image
    ])

    return np.concatenate([np.concatenate(row, axis=1) for row in full_image], axis=0)


def pretty_print(im):
    for row in im:
        print("".join(row))


def main():

    monster = """
                  # 
#    ##    ##    ###
 #  #  #  #  #  #   
"""

    monster_squares = sum(x == "#" for x in monster)
    monster = [list(line) for line in monster.strip(
        "\n").splitlines() if line.strip(" ") != ""]

    monster = np.array(monster)

    monster_height, monster_width = monster.shape

    full_image = get_full_image()

    for transformed in transforms(full_image):
        sightings = 0

        image_height, image_width = transformed.shape

        for dy in range(0, image_height - monster_height + 1):
            for dx in range(0, image_width - monster_width + 1):
                sub_image = transformed[dy:dy +
                                        monster_height, dx:dx+monster_width]

                if len(monster[monster == sub_image]) == monster_squares:
                    sightings += 1
        if sightings > 1:
            break

    non_monster_squares = len(
        full_image[full_image == "#"]) - (sightings * monster_squares)
    print(non_monster_squares)


if __name__ == "__main__":
    with open("inputs/day20.txt") as f:
        tiles_by_id = get_tiles(f.read())
        gtd = tiles_by_id.get

        tiles = list(tiles_by_id.keys())
        locked_in = {tiles[0]}

        main()
