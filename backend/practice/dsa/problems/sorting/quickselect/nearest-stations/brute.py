class Solution:
    def nearestStations(self, stations, k):
        return sorted(stations, key=lambda p: (p[0] ** 2 + p[1] ** 2, p[0], p[1]))[:k]
