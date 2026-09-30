class Solution:
    def onShelf(self, shelf, target):
        lo, hi = 0, len(shelf) - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            if shelf[mid] == target:
                return True
            if shelf[lo] == shelf[mid] == shelf[hi]:
                lo += 1
                hi -= 1
            elif shelf[lo] <= shelf[mid]:
                if shelf[lo] <= target < shelf[mid]:
                    hi = mid - 1
                else:
                    lo = mid + 1
            else:
                if shelf[mid] < target <= shelf[hi]:
                    lo = mid + 1
                else:
                    hi = mid - 1
        return False
