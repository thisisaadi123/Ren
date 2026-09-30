class Solution:
    def cubeRoot(self, volume):
        lo, hi = -max(1.0, abs(volume)), max(1.0, abs(volume))
        for _ in range(200):
            mid = (lo + hi) / 2
            if mid * mid * mid < volume:
                lo = mid
            else:
                hi = mid
        return (lo + hi) / 2
