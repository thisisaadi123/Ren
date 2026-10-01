class Solution:
    # Mistake: always steps to the best-looking stone among the next k.
    def bestScore(self, stones, k):
        n = len(stones)
        i, score = 0, stones[0]
        while i < n - 1:
            if i + k >= n - 1:
                score += stones[-1]
                break
            j = max(range(i + 1, i + k + 1), key=lambda x: stones[x])
            score += stones[j]
            i = j
        return score
