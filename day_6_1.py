def get_answers(group):
    return set(group.replace("\n", ""))

with open("inputs/day6.txt") as f:
    groups = [ x for x in f.read().split("\n\n") ]

    solution = sum( len(get_answers(group)) for group in  groups)
    print(solution)
    