class Solution:
    def nthBeat(self, n, a, b):
        l = a * b // math.gcd(a, b)
        lo, hi = 1, n * min(a, b)
        while lo < hi:
            mid = (lo + hi) // 2
            if mid // a + mid // b - mid // l >= n:
                hi = mid
            else:
                lo = mid + 1
        return lo % (10**9 + 7)
