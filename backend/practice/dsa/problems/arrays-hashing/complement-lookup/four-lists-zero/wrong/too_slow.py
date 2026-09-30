class Solution:
    # Correct but O(n^3) with a lookup: too slow at n = 500 in Python.
    def countZeroQuads(self, a, b, c, d):
        dc = collections.Counter(d)
        return sum(dc[-(w + x + y)] for w in a for x in b for y in c)
