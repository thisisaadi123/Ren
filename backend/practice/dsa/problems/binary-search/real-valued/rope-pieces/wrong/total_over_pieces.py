class Solution:
    # Mistake: pretends leftover bits from different ropes can be joined.
    def longestPiece(self, ropes, pieces):
        return sum(ropes) / pieces
