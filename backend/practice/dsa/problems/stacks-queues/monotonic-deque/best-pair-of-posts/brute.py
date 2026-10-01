class Solution:
    def bestPair(self, posts, k):
        best = None
        for j in range(len(posts)):
            for i in range(j):
                if posts[j][0] - posts[i][0] <= k:
                    v = posts[i][1] + posts[j][1] + posts[j][0] - posts[i][0]
                    if best is None or v > best:
                        best = v
        return best
