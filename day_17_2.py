from collections import defaultdict
import itertools

world = defaultdict(
    lambda: defaultdict(
        lambda: defaultdict(
            lambda: defaultdict(int)
        )
    )
)

def is_active(x,y,z,w):
    return world[x][y][z][w] == 1

def get_all_points(world):
    points = []
    for x in world.keys():
        for y in world[x].keys():
            for z in world[x][y].keys():
                for w in world[x][y][z].keys():
                    if is_active(x,y,z,w):
                        points.append((x,y,z,w))
    return points

def get_neighbours(x, y, z, w):
    return list(map(
        lambda coordinate: (coordinate[0] + x, coordinate[1] + y, coordinate[2] + z, coordinate[3] + w),
        filter(
            lambda coordinate: coordinate != (0,0,0,0),
            itertools.product([-1, 0, 1], [-1, 0, 1], [-1, 0, 1], [-1, 0, 1])
        )
    ))

def get_number_active_neighbours(x,y,z,w):
    return sum( is_active(*neighbour) for neighbour in get_neighbours(x,y,z,w) )

def should_die(x,y,z,w):
    return get_number_active_neighbours(x,y,z,w) not in (2,3)
    
def should_born(x,y,z,w):
    return get_number_active_neighbours(x,y,z,w) == 3

with open("inputs/day17.txt") as f:
    z = 0
    w = 0
    for y, line in enumerate(f):
        for x, char in enumerate(line):
            if char == "#":
                world[x][y][z][w] = 1

def simulate():
    for iteration in range(6):
        considered = set()
        deaths = set()
        births = set()

        for point in get_all_points(world):
            if should_die(*point):
                deaths.add(point)

            for neighbour in get_neighbours(*point):
                if neighbour not in considered:
                    considered.add(neighbour)
                    if should_born(*neighbour):
                        births.add(neighbour)
        
        for point in deaths:
            (x,y,z,w) = point
            del world[x][y][z][w]
        for point in births:
            (x,y,z,w) = point
            world[x][y][z][w] = 1

simulate()

num_points = len(get_all_points(world))
print(num_points)