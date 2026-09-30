class Solution:
    # Mistake: starts a new pool at every column that is higher than its left neighbour's water surface.
    def largestPool(self, walls):
        n = len(walls)
        lm, rm = [0] * n, [0] * n
        for i in range(n):
            lm[i] = max(walls[i], lm[i - 1] if i else 0)
        for i in range(n - 1, -1, -1):
            rm[i] = max(walls[i], rm[i + 1] if i + 1 < n else 0)
        best = run = 0
        for i in range(n):
            w = min(lm[i], rm[i]) - walls[i]
            if i and walls[i] > walls[i - 1]:
                run = 0
            run += w
            best = max(best, run)
        return best
