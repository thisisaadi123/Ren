class Solution:
    # Mistake: puts every new station into the single biggest gap.
    def smallestMaxGap(self, stations, extra):
        gaps = sorted(b - a for a, b in zip(stations, stations[1:]))
        rest = gaps[-2] if len(gaps) > 1 else 0
        return max(rest, gaps[-1] / (extra + 1))
