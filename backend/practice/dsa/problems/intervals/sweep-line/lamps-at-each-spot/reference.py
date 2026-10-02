from bisect import bisect_left, bisect_right


class Solution:
    def lampsAt(self, lamps, spots):
        starts = sorted(s for s, _ in lamps)
        ends = sorted(e for _, e in lamps)
        return [bisect_right(starts, p) - bisect_left(ends, p) for p in spots]
