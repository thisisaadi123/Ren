class Solution:
    # Mistake: checks the span but not repeats.
    def isStraight(self, cards):
        return max(cards) - min(cards) + 1 == len(cards)
