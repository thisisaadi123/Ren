class Solution:
    def countZeroQuads(self, a, b, c, d):
        first = collections.Counter(x + y for x in a for y in b)
        return sum(first[-(x + y)] for x in c for y in d)
