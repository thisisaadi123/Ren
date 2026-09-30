class Solution:
    def biggestTank(self, posts):
        n = len(posts)
        best = 0
        for i in range(n):
            for j in range(i + 1, n):
                best = max(best, (j - i) * min(posts[i], posts[j]))
        return best
