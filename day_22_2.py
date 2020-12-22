from collections import deque


def get_decks(fread):
    p1, p2 = fread.split("\n\n")
    def parse(p): return deque(int(x) for x in p.splitlines()[1:])
    return parse(p1), parse(p2)


with open("inputs/day22.txt") as f:
    deck_1, deck_2 = get_decks(f.read())

    def do_game(d1, d2):
        previous_configurations = set()

        while len(d1) > 0 and len(d2) > 0:

            if (conf := (tuple(d1), tuple(d2))) in previous_configurations:
                return d1, 1  # Prevent loops
            else:
                previous_configurations.add(conf)

            card_1, card_2 = d1.popleft(), d2.popleft()

            if len(d1) >= card_1 and len(d2) >= card_2:
                d1_sub = deque(list(d1)[:card_1])
                d2_sub = deque(list(d2)[:card_2])
                _, round_winner = do_game(d1_sub, d2_sub)
            else:
                round_winner = 1 if card_1 > card_2 else 2

            if round_winner == 1:
                d1.append(card_1)
                d1.append(card_2)
            else:
                d2.append(card_2)
                d2.append(card_1)

        return d1 if len(d1) > 0 else d2, 1 if len(d1) > 0 else 2

    winning_deck, _ = do_game(deck_1, deck_2)

    score = sum((i + 1) * x for i, x in enumerate(reversed(winning_deck)))
    print(score)
