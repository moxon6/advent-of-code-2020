from llist import dllist

NUM_MOVES = 100
NUM_CUPS = 9


def wrap_decrement(x):
    return 1 + ((x-2) % NUM_CUPS)


def get_destination_cup_value(current_cup_value, next_three):
    destination = wrap_decrement(current_cup_value)
    while destination in next_three:
        destination = wrap_decrement(destination)

    return destination


def get_next_cup(cup):
    if cup == cup.owner().last:
        return cup.owner().first
    else:
        return cup.next


with open("inputs/day23.txt") as f:
    cups = dllist([int(x) for x in f.readline()])

    value_to_node = {x: cups.nodeat(i) for i, x in enumerate(cups)}

    current_cup = cups.first

    for move in range(NUM_MOVES):

        next_1 = get_next_cup(current_cup)
        next_2 = get_next_cup(next_1)
        next_3 = get_next_cup(next_2)

        cups.remove(next_1)
        cups.remove(next_2)
        cups.remove(next_3)

        destination_cup_value = get_destination_cup_value(
            current_cup.value,
            [next_1.value, next_2.value, next_3.value]
        )

        destination_cup_node = value_to_node[destination_cup_value]

        cups.insertnode(next_1, get_next_cup(destination_cup_node))
        cups.insertnode(next_2, next_1.next)
        cups.insertnode(next_3, next_2.next)

        current_cup = get_next_cup(current_cup)

    digits = []
    current_node = value_to_node[1]
    while ((current_node := get_next_cup(current_node)) != value_to_node[1]):
        digits.append(current_node.value)

    print("Solution:", "".join(str(x) for x in digits))
