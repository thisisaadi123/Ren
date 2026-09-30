class Solution:
    def countZeroQuads(self, a, b, c, d):
        return sum(1 for w in a for x in b for y in c for z in d if w + x + y + z == 0)
