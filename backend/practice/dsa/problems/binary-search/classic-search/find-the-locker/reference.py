class Solution:
    def findLocker(self, lockers, target):
        lo, hi = 0, len(lockers) - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            if lockers[mid] == target:
                return mid
            if lockers[mid] < target:
                lo = mid + 1
            else:
                hi = mid - 1
        return -1
