class Solution:
    def isPerfectSquare(self, tiles):
        lo, hi = 1, tiles
        while lo <= hi:
            mid = (lo + hi) // 2
            sq = mid * mid
            if sq == tiles:
                return True
            if sq < tiles:
                lo = mid + 1
            else:
                hi = mid - 1
        return False
