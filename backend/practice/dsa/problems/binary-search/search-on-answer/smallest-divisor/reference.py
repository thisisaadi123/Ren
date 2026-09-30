class Solution:
    def smallestDivisor(self, loads, threshold):
        lo, hi = 1, max(loads)
        while lo < hi:
            mid = (lo + hi) // 2
            if sum((x + mid - 1) // mid for x in loads) <= threshold:
                hi = mid
            else:
                lo = mid + 1
        return lo
