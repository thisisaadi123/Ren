class Solution:
    def widestGap(self, nums):
        n = len(nums)
        lo, hi = min(nums), max(nums)
        if n < 2 or lo == hi:
            return 0
        size = max(1, (hi - lo) // (n - 1))
        count = (hi - lo) // size + 1
        bmin = [None] * count
        bmax = [None] * count
        for x in nums:
            b = (x - lo) // size
            if bmin[b] is None or x < bmin[b]:
                bmin[b] = x
            if bmax[b] is None or x > bmax[b]:
                bmax[b] = x
        best, prev = 0, lo
        for b in range(count):
            if bmin[b] is not None:
                best = max(best, bmin[b] - prev)
                prev = bmax[b]
        return best
