from collections import deque


class Solution:
    def bestPair(self, posts, k):
        dq = deque()
        best = None
        for j, (x, y) in enumerate(posts):
            while dq and x - posts[dq[0]][0] > k:
                dq.popleft()
            if dq:
                xi, yi = posts[dq[0]]
                value = y + x + yi - xi
                if best is None or value > best:
                    best = value
            while dq and posts[dq[-1]][1] - posts[dq[-1]][0] <= y - x:
                dq.pop()
            dq.append(j)
        return best
