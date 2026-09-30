class Solution:
    # Mistake: goes past an equal score instead of returning its position.
    def insertPosition(self, scores, target):
        lo, hi = 0, len(scores)
        while lo < hi:
            mid = (lo + hi) // 2
            if scores[mid] <= target:
                lo = mid + 1
            else:
                hi = mid
        return lo
