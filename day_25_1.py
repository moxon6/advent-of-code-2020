import itertools


def op(value, subject_number):
    return (value * subject_number) % 20201227


with open("inputs/day25.txt") as f:
    card_public_key = int(f.readline())
    door_public_key = int(f.readline())
    loop_sizes = {}

    value = 1
    for i in itertools.count(start=1):
        value = op(value, 7)
        if value in [card_public_key, door_public_key]:
            loop_sizes[value] = i
            if len(loop_sizes) == 2:
                break

    value = 1
    for i in range(loop_sizes[door_public_key]):
        value = op(value, card_public_key)
    print(value)
