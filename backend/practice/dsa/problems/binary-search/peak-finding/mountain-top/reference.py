class Solution:
    def mountainTop(self, elevations):
        lo, hi = 0, len(elevations) - 1
        while lo < hi:
            mid = (lo + hi) // 2
            if elevations[mid] < elevations[mid + 1]:
                lo = mid + 1
            else:
                hi = mid
        return lo
