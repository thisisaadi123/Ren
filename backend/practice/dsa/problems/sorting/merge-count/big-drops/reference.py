class Solution:
    def countBigDrops(self, prices):
        a = prices[:]
        n = len(a)
        buf = [0] * n
        total = 0
        width = 1
        while width < n:
            for lo in range(0, n, 2 * width):
                mid, hi = min(lo + width, n), min(lo + 2 * width, n)
                j = mid
                for i in range(lo, mid):
                    while j < hi and a[i] > 2 * a[j]:
                        j += 1
                    total += j - mid
                buf[lo:hi] = sorted(a[lo:hi])
            a, buf = buf, a
            width *= 2
        return total
