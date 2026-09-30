class Solution:
    # Mistake: uses |x| + |y| instead of straight-line distance.
    def nearestStations(self, stations, k):
        return sorted(stations, key=lambda p: (abs(p[0]) + abs(p[1]), p[0], p[1]))[:k]
