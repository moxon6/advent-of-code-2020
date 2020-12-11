def pretty_print(grid):
    for row in grid:
        print("".join(row))

relative_coordinates = [
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1)
]

def get_total_occupied(grid):
    return sum(
        sum( 1 for seat in row if seat == "#")
        for row in grid
    )

with open("inputs/day11.txt") as f:
    grid = [list(x.strip()) for x in f.readlines()]

    def seat_exists(i, j):
        return 0 <= i < len(grid) and 0 <= j < len(grid[0])
    
    def get_adjacent_seats(i,j):
        return filter(
            lambda x: seat_exists(*x),
            map(
                lambda x: (x[0] + i, x[1] + j),
                relative_coordinates
            )
        )

    while True:
        changes = []
        for i, row in enumerate(grid):
            for j, seat in enumerate(row):

                num_occupied = sum( 1 for (x,y) in get_adjacent_seats(i,j) if grid[x][y] == "#" )

                if seat == "L" and num_occupied == 0:
                    changes.append((i,j))
                elif seat == "#" and num_occupied >= 4:
                    changes.append((i,j))

        if len(changes) == 0:
            print("Total occupied", get_total_occupied(grid))
            break
        else:
            for (i,j) in changes:
                grid[i][j] = "L" if grid[i][j] == "#" else "#"
                

                        
