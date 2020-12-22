from collections import deque


def get_decks(fread):
    p1, p2 = fread.split("\n\n")
    def parse(p): return deque(int(x) for x in p.splitlines()[1:])
    return parse(p1), parse(p2)


with open("inputs/day22.txt") as f:
    deck_1, deck_2 = get_decks(f.read())

    def do_game(d1, d2):
        while len(d1) > 0 and len(d2) > 0:
            card_1, card_2 = d1.popleft(), d2.popleft()
            if card_1 > card_2:
                d1.append(card_1)
                d1.append(card_2)
            else:
                d2.append(card_2)
                d2.append(card_1)
        winner = 1 if len(deck_1) > 0 else 2

        return d1, d2, winner

    deck_1, deck_2, winner = do_game(deck_1, deck_2)
    winning_deck = (deck_1, deck_1)[winner - 1]
    score = sum((i + 1) * x for i, x in enumerate(reversed(winning_deck)))
    print(score)
