import heapq


class Solution:
    def cheapestPairs(self, a, b, k):
        h = [(a[0] + b[0], 0, 0)]
        out = []
        while len(out) < k:
            s, i, j = heapq.heappop(h)
            out.append(s)
            if j + 1 < len(b):
                heapq.heappush(h, (a[i] + b[j + 1], i, j + 1))
            if j == 0 and i + 1 < len(a):
                heapq.heappush(h, (a[i + 1] + b[0], i + 1, 0))
        return out
