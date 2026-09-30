class Solution:
    def kthFree(self, taken, k):
        lo, hi = 0, len(taken)
        while lo < hi:
            mid = (lo + hi) // 2
            if taken[mid] - (mid + 1) < k:
                lo = mid + 1
            else:
                hi = mid
        return lo + k
