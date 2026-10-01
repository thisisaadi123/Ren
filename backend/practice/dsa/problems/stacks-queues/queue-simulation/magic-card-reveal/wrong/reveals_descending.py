from collections import deque


class Solution:
    # Mistake: fills the positions with the largest cards first.
    def stackDeck(self, cards):
        n = len(cards)
        spots = deque(range(n))
        out = [0] * n
        for card in sorted(cards, reverse=True):
            out[spots.popleft()] = card
            if spots:
                spots.append(spots.popleft())
        return out
