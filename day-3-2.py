
def get_solution(dx, dy):
    with open("inputs/day3.txt") as f:
        position = 0
        trees = 0
        for (index, line) in enumerate(f.read().splitlines()):
            if (index % dy == 0):
                if line[position] == "#":
                    trees += 1
                position = (position + dx) % len(line)
        return trees

product = 1
product *= get_solution(1, 1)
product *= get_solution(3, 1)
product *= get_solution(5, 1)
product *= get_solution(7, 1)
product *= get_solution(1, 2)
print(product)