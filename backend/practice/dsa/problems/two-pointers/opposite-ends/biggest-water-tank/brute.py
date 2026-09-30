class Solution:
    def biggestTank(self, posts):
        n = len(posts)
        return max((j - i) * min(posts[i], posts[j]) for i in range(n) for j in range(i + 1, n))
