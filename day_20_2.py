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




def get_full_image():
    def get_adjacent_in_direction(tile, match_direction):

        cache = function_to_cache[match_direction]
        if tile.id in cache:
            cached_tile_id = cache[tile.id]
            return tiles_by_id[cached_tile_id]

        for candidate in tiles:
            if (tile is candidate):
                continue

            if candidate.id in locked_in:
                if match_direction(tile.data, candidate.data):
                    return candidate
            else:
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

        def get_and_transform_adjacent_tiles(tile):
            return [ get_adjacent_in_direction(tile, direction) for direction in match_directions ]
            
        locked_in = set([ tiles[0].id ])
        frontier = [ tiles[0] ]

        go_left = {}
        go_right = {}
        go_up = {}
        go_down = {}

        tiles_by_id = {
            tile.id: tile 
            for tile in tiles
        }

        function_to_cache = {
            matches_left: go_left,
            matches_right: go_right,
            matches_up: go_up,
            matches_down: go_down
        }

        while len(frontier) > 0:

            new_frontier = []
            
            for frontier_tile in frontier:
                (left, right, up, down) = get_and_transform_adjacent_tiles(frontier_tile)
                if left is not None and left.id not in locked_in:
                    go_left[frontier_tile.id] = left.id
                    go_right[left.id] = frontier_tile.id
                    if left not in new_frontier:
                        new_frontier.append(left)
                if right is not None and right.id not in locked_in:
                    go_right[frontier_tile.id] = right.id
                    go_left[right.id] = frontier_tile.id
                    if right not in new_frontier:
                        new_frontier.append(right)
                if up is not None and up.id not in locked_in:
                    go_up[frontier_tile.id] = up.id
                    go_down[up.id] = frontier_tile.id
                    if up not in new_frontier:
                        new_frontier.append(up)
                if down is not None and down.id not in locked_in:
                    go_down[frontier_tile.id] = down.id
                    go_up[down.id] = frontier_tile.id
                    if down not in new_frontier:
                        new_frontier.append(down)

            frontier = new_frontier
            for f in new_frontier:
                locked_in.add(f.id)
        
        top_left = tiles[0].id
        while go_left.get(top_left, None) is not None:
            top_left = go_left.get(top_left)
        while go_up.get(top_left, None) is not None:
            top_left = go_up.get(top_left)
        
        start_of_line = top_left
        image = []

        while True: # Do while
            current_tile = start_of_line
            image.append([ start_of_line ])
            
            while True: # Do while
                current_tile = go_right.get(current_tile)
                image[-1].append(current_tile)
                if go_right.get(current_tile, None) is None:
                    break
            
            if go_down.get(start_of_line, None) is None:
                break

            start_of_line = go_down.get(start_of_line)
        
        image = np.array(image)
        # print(image)

        def trim_edges(arr):
            arr = arr[::-1] # TODO: Remove reverse
            return arr[1:-1, 1:-1]

        full_image = np.array([
            [ trim_edges(tiles_by_id[id].data) for id in row] for row in image[::-1] # TODO: Remove reverse
        ])

        return np.concatenate([ np.concatenate(row, axis=1) for row in full_image ], axis=0)

def pretty_print(im):
    for row in im:
        print("".join(row))

def main():

    monster = """
                  # 
#    ##    ##    ###
 #  #  #  #  #  #   
"""

    monster_squares = sum( x == "#" for x in monster)
    monster = [ list(line) for line in monster.strip("\n").splitlines() if line.strip(" ") != "" ]

    monster = np.array(monster)

    monster_height, monster_width = monster.shape
    
    
    full_image = get_full_image()
    
    for transformed in transforms(full_image):
        sightings = 0
        
        image_height, image_width = transformed.shape

        for dy in range(0, image_height - monster_height + 1):
            for dx in range(0, image_width - monster_width + 1):
                sub_image = transformed[dy:dy+monster_height, dx:dx+monster_width]

                if len( monster[monster == sub_image] ) == monster_squares:
                    sightings += 1
        if sightings > 1:
            break
    
    non_monster_squares = len(full_image[full_image == "#"]) - (sightings * monster_squares)
    print(non_monster_squares)
    
if __name__ == "__main__":
    main()

