import numpy as np

direction_map = {
    "N": np.array([0,1]),
    "S": np.array([0,-1]),
    "E": np.array([1, 0]),
    "W": np.array([-1, 0])
}

def rotate(x, y, theta):
    theta = np.radians(theta)
    ctheta, stheta = np.cos(theta), np.sin(theta)
    return np.array([ x * ctheta -  y * stheta, x * stheta + y * ctheta ]).astype(int)

position = np.array([0, 0])
direction = np.array([ 1, 0 ]) # east

with open("inputs/day12.txt") as f:
    for instruction in f.readlines():
        operation, magnitude = instruction[0], int(instruction[1:])
        if operation in direction_map:
            position += direction_map[operation] * magnitude
        elif operation == "F":
            position += direction * magnitude
        elif operation == "L":
            direction = rotate(*direction, magnitude)
        elif operation == "R":
            direction = rotate(*direction, -magnitude)

print(np.sum( np.abs(position) ))