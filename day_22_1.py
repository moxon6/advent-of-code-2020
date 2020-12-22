from collections import deque


def get_decks(fread):
    p1, p2 = fread.split("\n\n")
    def parse(p): return deque(int(x) for x in p.splitlines()[1:])
    return parse(p1), parse(p2)


with open("inputs/day22.txt") as f:
    deck_1, deck_2 = get_decks(f.read())

    while len(deck_1) > 0 and len(deck_2) > 0:
        card_1, card_2 = deck_1.popleft(), deck_2.popleft()
        if card_1 > card_2:
            deck_1.append(card_1)
            deck_1.append(card_2)
        else:
            deck_2.append(card_2)
            deck_2.append(card_1)

    winning_deck = deck_1 if len(deck_1) > 0 else deck_2

    score = sum((i + 1) * x for i, x in enumerate(reversed(winning_deck)))

    print(score)
