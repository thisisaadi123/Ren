class Solution:
    # Mistake: counts numbers divisible by both a and b twice.
    def nthBeat(self, n, a, b):
        lo, hi = 1, n * min(a, b)
        while lo < hi:
            mid = (lo + hi) // 2
            if mid // a + mid // b >= n:
                hi = mid
            else:
                lo = mid + 1
        return lo % (10**9 + 7)
