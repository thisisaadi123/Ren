class Solution:
    def isStraight(self, cards):
        return len(set(cards)) == len(cards) and max(cards) - min(cards) + 1 == len(cards)
