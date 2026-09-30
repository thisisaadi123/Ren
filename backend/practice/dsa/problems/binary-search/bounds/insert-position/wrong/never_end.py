class Solution:
    # Mistake: hi starts at n - 1, so it can't answer "after the last score".
    def insertPosition(self, scores, target):
        lo, hi = 0, len(scores) - 1
        while lo < hi:
            mid = (lo + hi) // 2
            if scores[mid] < target:
                lo = mid + 1
            else:
                hi = mid
        return lo
