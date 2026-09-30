class Solution:
    # Mistake: only tries whole-number lengths.
    def longestPiece(self, ropes, pieces):
        lo, hi = 0, max(ropes)
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if sum(r // mid for r in ropes) >= pieces:
                lo = mid
            else:
                hi = mid - 1
        return float(lo)
