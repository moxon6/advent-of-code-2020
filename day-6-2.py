def get_answers(group):
    answer_set = set(group.replace("\n", ""))

    return sum( 
        int(all(answer in member for member in group.splitlines()))
        for answer in answer_set
    )
            

with open("inputs/day6.txt") as f:
    groups = [ x for x in f.read().split("\n\n") ]

    solution = sum( get_answers(group) for group in  groups)
    print(solution)
    