class Solution:
    # Mistake: returns all the water, not the largest single pool.
    def largestPool(self, walls):
        n = len(walls)
        lm, rm = [0] * n, [0] * n
        for i in range(n):
            lm[i] = max(walls[i], lm[i - 1] if i else 0)
        for i in range(n - 1, -1, -1):
            rm[i] = max(walls[i], rm[i + 1] if i + 1 < n else 0)
        return sum(min(lm[i], rm[i]) - walls[i] for i in range(n))
