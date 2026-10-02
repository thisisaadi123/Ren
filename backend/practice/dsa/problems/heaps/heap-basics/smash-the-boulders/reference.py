import heapq


class Solution:
    def lastBoulder(self, boulders):
        h = [-w for w in boulders]
        heapq.heapify(h)
        while len(h) > 1:
            a, b = -heapq.heappop(h), -heapq.heappop(h)
            if a != b:
                heapq.heappush(h, -(a - b))
        return -h[0] if h else 0
