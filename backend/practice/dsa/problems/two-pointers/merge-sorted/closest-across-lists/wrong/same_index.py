class Solution:
    # Mistake: only compares values at the same position.
    def closestAcross(self, a, b):
        return min(abs(x - y) for x, y in zip(a, b))
