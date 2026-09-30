class Solution:
    def sortedSquares(self, values):
        return sorted(v * v for v in values)
