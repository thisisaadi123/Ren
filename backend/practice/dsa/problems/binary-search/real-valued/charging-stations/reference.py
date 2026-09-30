class Solution:
    def smallestMaxGap(self, stations, extra):
        gaps = [b - a for a, b in zip(stations, stations[1:])]
        lo, hi = 0.0, float(max(gaps))
        for _ in range(100):
            mid = (lo + hi) / 2
            if mid > 0 and sum(math.ceil(g / mid) - 1 for g in gaps) <= extra:
                hi = mid
            else:
                lo = mid
        return hi
