print(sum( 1 for (index, line) in enumerate(open("inputs/day3.txt").read().splitlines()) if line[(index * 3) % len(line)] == "#" ))
