from collections import deque


class Solution:
    # Mistake: moves a card to the bottom BEFORE revealing, instead of after.
    def stackDeck(self, cards):
        n = len(cards)
        spots = deque(range(n))
        out = [0] * n
        for card in sorted(cards):
            if len(spots) > 1:
                spots.append(spots.popleft())
            out[spots.popleft()] = card
        return out
