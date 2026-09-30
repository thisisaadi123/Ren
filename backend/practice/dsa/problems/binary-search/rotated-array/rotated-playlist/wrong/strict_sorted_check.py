class Solution:
    # Mistake: uses < instead of <= to detect the sorted left half, which breaks when lo == mid.
    def findTrack(self, playlist, target):
        lo, hi = 0, len(playlist) - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            if playlist[mid] == target:
                return mid
            if playlist[lo] < playlist[mid]:
                if playlist[lo] <= target < playlist[mid]:
                    hi = mid - 1
                else:
                    lo = mid + 1
            else:
                if playlist[mid] < target <= playlist[hi]:
                    lo = mid + 1
                else:
                    hi = mid - 1
        return -1
