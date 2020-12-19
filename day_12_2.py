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
    return np.array([ x * ctheta -  y * stheta, x * stheta + y * ctheta ])

position = np.array([0, 0], dtype=float)
waypoint_relative_position = np.array([10, 1], dtype=float)

with open("inputs/day12.txt") as f:
    for instruction in f.readlines():
        operation, magnitude = instruction[0], int(instruction[1:])
        if operation in direction_map:
            waypoint_relative_position += direction_map[operation] * magnitude
        elif operation == "F":
            position += (waypoint_relative_position) * magnitude
        elif operation == "L":
            waypoint_relative_position = rotate(*(waypoint_relative_position), magnitude)
        elif operation == "R":
            waypoint_relative_position = rotate(*(waypoint_relative_position), -magnitude)
print(int(np.sum( np.abs(position) )))