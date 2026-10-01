class Solution:
    # Mistake: only pairs neighbouring posts.
    def bestPair(self, posts, k):
        best = None
        for i in range(len(posts) - 1):
            (x1, y1), (x2, y2) = posts[i], posts[i + 1]
            if x2 - x1 <= k:
                v = y1 + y2 + x2 - x1
                if best is None or v > best:
                    best = v
        return best
