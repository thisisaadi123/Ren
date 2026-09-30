class Solution:
    def minTimeForRounds(self, roundTime, totalRounds):
        lo, hi = 1, min(roundTime) * totalRounds
        while lo < hi:
            mid = (lo + hi) // 2
            if sum(mid // t for t in roundTime) >= totalRounds:
                hi = mid
            else:
                lo = mid + 1
        return lo
