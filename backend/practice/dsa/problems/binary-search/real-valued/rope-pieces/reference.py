class Solution:
    def longestPiece(self, ropes, pieces):
        lo, hi = 0.0, float(max(ropes))
        for _ in range(100):
            mid = (lo + hi) / 2
            if mid > 0 and sum(int(r / mid) for r in ropes) >= pieces:
                lo = mid
            else:
                hi = mid
        return lo
