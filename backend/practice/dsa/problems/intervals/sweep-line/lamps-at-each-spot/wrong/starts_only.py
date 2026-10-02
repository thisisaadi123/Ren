from bisect import bisect_right


class Solution:
    # Mistake: counts lamps that have started, forgetting the ones that already ended.
    def lampsAt(self, lamps, spots):
        starts = sorted(s for s, _ in lamps)
        return [bisect_right(starts, p) for p in spots]
