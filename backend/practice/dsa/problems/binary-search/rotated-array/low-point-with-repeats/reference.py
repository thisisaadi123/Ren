class Solution:
    def lowestWithRepeats(self, readings):
        lo, hi = 0, len(readings) - 1
        while lo < hi:
            mid = (lo + hi) // 2
            if readings[mid] > readings[hi]:
                lo = mid + 1
            elif readings[mid] < readings[hi]:
                hi = mid
            else:
                hi -= 1
        return readings[lo]
