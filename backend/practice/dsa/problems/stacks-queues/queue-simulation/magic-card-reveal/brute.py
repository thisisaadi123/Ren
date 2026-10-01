from itertools import permutations


class Solution:
    def stackDeck(self, cards):
        want = sorted(cards)
        for order in permutations(cards):
            deck = list(order)
            shown = []
            while deck:
                shown.append(deck.pop(0))
                if deck:
                    deck.append(deck.pop(0))
            if shown == want:
                return list(order)
