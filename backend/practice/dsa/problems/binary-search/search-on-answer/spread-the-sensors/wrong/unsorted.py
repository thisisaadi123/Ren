class Solution:
    # Mistake: runs the greedy placement without sorting the spots first.
    def widestSpacing(self, spots, sensors):
        def fits(gap):
            placed, last = 1, spots[0]
            for x in spots[1:]:
                if x - last >= gap:
                    placed += 1
                    last = x
            return placed >= sensors
        lo, hi = 1, max(spots) - min(spots)
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if fits(mid):
                lo = mid
            else:
                hi = mid - 1
        return lo
