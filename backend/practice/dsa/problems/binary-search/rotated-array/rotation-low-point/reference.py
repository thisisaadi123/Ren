class Solution:
    def lowestReading(self, readings):
        lo, hi = 0, len(readings) - 1
        while lo < hi:
            mid = (lo + hi) // 2
            if readings[mid] > readings[hi]:
                lo = mid + 1
            else:
                hi = mid
        return readings[lo]
