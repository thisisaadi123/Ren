class Solution:
    def isPerfectSquare(self, tiles):
        r = 1
        while r * r < tiles:
            r += 1
        return r * r == tiles
