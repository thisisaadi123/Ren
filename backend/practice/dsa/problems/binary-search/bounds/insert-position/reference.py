class Solution:
    def insertPosition(self, scores, target):
        lo, hi = 0, len(scores)
        while lo < hi:
            mid = (lo + hi) // 2
            if scores[mid] < target:
                lo = mid + 1
            else:
                hi = mid
        return lo
