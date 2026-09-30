class Solution:
    def smallestWithZeros(self, zeros):
        def z(n):
            total = 0
            while n:
                n //= 5
                total += n
            return total
        if zeros == 0:
            return 0
        hi = 1
        while z(hi) < zeros:
            hi *= 2
        lo = hi // 2
        while lo < hi:
            mid = (lo + hi) // 2
            if z(mid) >= zeros:
                hi = mid
            else:
                lo = mid + 1
        return lo
