class Solution:
    # Mistake: keeps ties in input order.
    def nearestStations(self, stations, k):
        return sorted(stations, key=lambda p: p[0] ** 2 + p[1] ** 2)[:k]
