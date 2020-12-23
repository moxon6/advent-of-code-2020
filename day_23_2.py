from llist import dllist

NUM_MOVES = 10 * 1000 * 1000
NUM_CUPS = 1000 * 1000


def wrap_decrement(x):
    return x - 1 if x > 1 else NUM_CUPS


def get_destination_cup(current_cup, next_three):
    destination_value = wrap_decrement(current_cup.value)
    while destination_value in {x.value for x in next_three}:
        destination_value = wrap_decrement(destination_value)
    return value_to_node[destination_value]


def get_next_cup(cup):
    return cup.next if cup.next else cup.owner().first


def get_next_three_cups(cup):
    next_1 = get_next_cup(cup)
    next_2 = get_next_cup(next_1)
    next_3 = get_next_cup(next_2)
    return [next_1, next_2, next_3]


def get_cups():
    with open("inputs/day23.txt") as f:
        cups = [int(x) for x in f.readline()]
        cups.extend(range(len(cups) + 1, NUM_CUPS + 1))
        return dllist(cups)


cups = get_cups()
value_to_node = {x: cups.nodeat(i) for i, x in enumerate(cups)}

current_cup = cups.first
for move in range(NUM_MOVES):
    next_cups = get_next_three_cups(current_cup)

    for cup in next_cups:
        cups.remove(cup)

    insert_after = get_destination_cup(current_cup, next_cups)

    for cup in next_cups:
        insert_after = cups.insertnode(cup, get_next_cup(insert_after))

    current_cup = get_next_cup(current_cup)

one_node = value_to_node[1]

after_one = get_next_cup(one_node)
after_two = get_next_cup(after_one)

print("Solution:", after_one.value * after_two.value)
