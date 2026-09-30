class Solution:
    def kthPairGap(self, heights, k):
        h = sorted(heights)
        n = len(h)

        def pairs_within(d):
            total = left = 0
            for right in range(n):
                while h[right] - h[left] > d:
                    left += 1
                total += right - left
            return total

        lo, hi = 0, h[-1] - h[0]
        while lo < hi:
            mid = (lo + hi) // 2
            if pairs_within(mid) >= k:
                hi = mid
            else:
                lo = mid + 1
        return lo
