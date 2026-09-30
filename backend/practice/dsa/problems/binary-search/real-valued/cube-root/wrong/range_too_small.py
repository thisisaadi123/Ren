class Solution:
    # Mistake: searches only up to |volume|, which misses roots of numbers between -1 and 1.
    def cubeRoot(self, volume):
        lo, hi = -abs(volume), abs(volume)
        for _ in range(200):
            mid = (lo + hi) / 2
            if mid * mid * mid < volume:
                lo = mid
            else:
                hi = mid
        return lo
