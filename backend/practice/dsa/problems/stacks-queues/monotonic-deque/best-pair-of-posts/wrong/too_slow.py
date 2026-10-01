class Solution:
    # Mistake: tries every pair within reach: O(n^2) when k is large.
    def bestPair(self, posts, k):
        best = None
        for j in range(len(posts)):
            xj, yj = posts[j]
            for i in range(j - 1, -1, -1):
                xi, yi = posts[i]
                if xj - xi > k:
                    break
                v = yi + yj + xj - xi
                if best is None or v > best:
                    best = v
        return best
