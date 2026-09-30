class Solution:
    def widestSpacing(self, spots, sensors):
        s = sorted(spots)

        def fits(gap):
            placed, last = 1, s[0]
            for x in s[1:]:
                if x - last >= gap:
                    placed += 1
                    last = x
            return placed >= sensors

        lo, hi = 1, (s[-1] - s[0]) // (sensors - 1)
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if fits(mid):
                lo = mid
            else:
                hi = mid - 1
        return lo
