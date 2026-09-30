class Solution:
    # Mistake: spreads the new stations as if the highway were empty.
    def smallestMaxGap(self, stations, extra):
        return (stations[-1] - stations[0]) / (len(stations) - 1 + extra)
