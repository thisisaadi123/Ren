class Solution:
    def bestScore(self, stones, k):
        n = len(stones)
        best = [None] * n
        best[0] = stones[0]
        for i in range(1, n):
            best[i] = stones[i] + max(best[j] for j in range(max(0, i - k), i))
        return best[-1]
