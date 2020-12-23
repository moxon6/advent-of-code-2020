NUM_MOVES = 100


def separate_next_three(cups, current_cup):
    current_cup_index = cups.index(current_cup)
    next_indices = [
        i % len(cups)
        for i in range(current_cup_index + 1, current_cup_index + 4)
    ]

    assert len(next_indices) == 3

    return [x for (i, x) in enumerate(cups) if i not in next_indices], [cups[i] for i in next_indices]


def wrap_decrement(x):
    return 1 + ((x-2) % 9)


def get_destination_cup(current_cup, next_three):
    destination = wrap_decrement(current_cup)
    while destination in next_three:
        destination = wrap_decrement(destination)

    return destination


with open("inputs/day23.txt") as f:
    cups = [int(x) for x in f.readline()]
    current_cup = cups[0]

    for move in range(NUM_MOVES):

        print("Move number", move + 1)
        print("Cups", cups)
        print("Current cup", current_cup)

        initial_length = len(cups)

        remaining_cups, next_three = separate_next_three(
            cups,
            current_cup
        )

        destination_cup = get_destination_cup(
            current_cup,
            next_three
        )
        print("Next three cups", next_three)
        print("Destination", destination_cup, "\n\n")

        destination_index = remaining_cups.index(destination_cup)
        cups = [
            *remaining_cups[:destination_index + 1],
            *next_three,
            *remaining_cups[destination_index+1:]
        ]

        current_cup_index = (cups.index(current_cup) + 1) % len(cups)
        current_cup = cups[current_cup_index]
    print("Final cups", cups)

    start_index = cups.index(1)
    digits = [
        cups[i % 9] for i in range(start_index + 1, start_index + 9)
    ]
    print("Solution:", "".join(str(x) for x in digits))
