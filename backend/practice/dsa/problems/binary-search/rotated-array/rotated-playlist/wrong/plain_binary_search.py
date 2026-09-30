class Solution:
    # Mistake: ignores the rotation.
    def findTrack(self, playlist, target):
        lo, hi = 0, len(playlist) - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            if playlist[mid] == target:
                return mid
            if playlist[mid] < target:
                lo = mid + 1
            else:
                hi = mid - 1
        return -1
