class Solution:
    def rowsNeeded(self, cans):
        hi = 1
        while hi * (hi + 1) // 2 < cans:
            hi *= 2
        lo = hi // 2
        while lo < hi:
            mid = (lo + hi) // 2
            if mid * (mid + 1) // 2 >= cans:
                hi = mid
            else:
                lo = mid + 1
        return lo
