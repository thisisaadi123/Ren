from bisect import bisect_right


class Solution:
    # Mistake: a lamp ending exactly at the spot is counted as off.
    def lampsAt(self, lamps, spots):
        starts = sorted(s for s, _ in lamps)
        ends = sorted(e for _, e in lamps)
        return [bisect_right(starts, p) - bisect_right(ends, p) for p in spots]
