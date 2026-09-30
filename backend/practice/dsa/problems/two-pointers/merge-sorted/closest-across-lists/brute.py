class Solution:
    def closestAcross(self, a, b):
        return min(abs(x - y) for x in a for y in b)
