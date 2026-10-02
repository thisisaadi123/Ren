import heapq


class Solution:
    # Mistake: drops repeated prices.
    def cheapestPairs(self, a, b, k):
        h, seen, out = [(a[0] + b[0], 0, 0)], {(0, 0)}, []
        while len(out) < k and h:
            s, i, j = heapq.heappop(h)
            if not out or out[-1] != s:
                out.append(s)
            for x, y in ((i + 1, j), (i, j + 1)):
                if x < len(a) and y < len(b) and (x, y) not in seen:
                    seen.add((x, y))
                    heapq.heappush(h, (a[x] + b[y], x, y))
        return out
