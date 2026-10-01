from collections import deque


class Solution:
    def stackDeck(self, cards):
        n = len(cards)
        spots = deque(range(n))
        out = [0] * n
        for card in sorted(cards):
            out[spots.popleft()] = card
            if spots:
                spots.append(spots.popleft())
        return out
