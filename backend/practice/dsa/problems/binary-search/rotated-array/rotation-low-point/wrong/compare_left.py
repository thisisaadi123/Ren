class Solution:
    # Mistake: compares with the left end, which fails when the list isn't rotated.
    def lowestReading(self, readings):
        lo, hi = 0, len(readings) - 1
        while lo < hi:
            mid = (lo + hi) // 2
            if readings[mid] >= readings[lo]:
                lo = mid + 1
            else:
                hi = mid
        return readings[lo]
