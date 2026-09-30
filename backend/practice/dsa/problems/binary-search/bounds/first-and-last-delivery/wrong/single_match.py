class Solution:
    # Mistake: returns the first match it lands on as both ends of the range.
    def deliveryRange(self, times, target):
        lo, hi = 0, len(times) - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            if times[mid] == target:
                return [mid, mid]
            if times[mid] < target:
                lo = mid + 1
            else:
                hi = mid - 1
        return [-1, -1]
