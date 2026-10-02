import heapq


class Solution:
    # Mistake: smashes the two lightest boulders.
    def lastBoulder(self, boulders):
        h = list(boulders)
        heapq.heapify(h)
        while len(h) > 1:
            a, b = heapq.heappop(h), heapq.heappop(h)
            if a != b:
                heapq.heappush(h, abs(a - b))
        return h[0] if h else 0
