class Solution:
    # Mistake: scans all k previous stones for every stone: O(n * k).
    def bestScore(self, stones, k):
        n = len(stones)
        best = [0] * n
        best[0] = stones[0]
        for i in range(1, n):
            m = None
            for j in range(max(0, i - k), i):
                if m is None or best[j] > m:
                    m = best[j]
            best[i] = stones[i] + m
        return best[-1]
