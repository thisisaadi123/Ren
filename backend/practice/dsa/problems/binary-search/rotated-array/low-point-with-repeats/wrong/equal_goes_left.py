class Solution:
    # Mistake: on equal values jumps hi to mid, which can skip past the minimum.
    def lowestWithRepeats(self, readings):
        lo, hi = 0, len(readings) - 1
        while lo < hi:
            mid = (lo + hi) // 2
            if readings[mid] > readings[hi]:
                lo = mid + 1
            else:
                hi = mid
        return readings[lo]
