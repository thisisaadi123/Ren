class Solution:
    # Mistake: checks repeats but not the span.
    def isStraight(self, cards):
        return len(set(cards)) == len(cards)
