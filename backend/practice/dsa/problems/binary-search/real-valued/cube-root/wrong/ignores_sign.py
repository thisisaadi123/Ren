class Solution:
    # Mistake: drops the sign, so negative volumes get a positive root.
    def cubeRoot(self, volume):
        v = abs(volume)
        lo, hi = 0.0, max(1.0, v)
        for _ in range(200):
            mid = (lo + hi) / 2
            if mid * mid * mid < v:
                lo = mid
            else:
                hi = mid
        return lo
