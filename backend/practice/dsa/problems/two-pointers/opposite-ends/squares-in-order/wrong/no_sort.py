class Solution:
    # Mistake: squares in place without reordering.
    def sortedSquares(self, values):
        return [v * v for v in values]
