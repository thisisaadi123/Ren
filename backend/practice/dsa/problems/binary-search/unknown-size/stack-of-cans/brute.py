class Solution:
    def rowsNeeded(self, cans):
        r = 0
        while r * (r + 1) // 2 < cans:
            r += 1
        return r
