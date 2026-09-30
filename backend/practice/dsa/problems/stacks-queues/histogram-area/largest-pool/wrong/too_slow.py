class Solution:
    # Mistake: finds the tallest wall on each side of every column by scanning: O(n²).
    def largestPool(self, walls):
        n = len(walls)
        best = run = 0
        for i in range(n):
            lm = max(walls[j] for j in range(i + 1))
            rm = max(walls[j] for j in range(i, n))
            w = min(lm, rm) - walls[i]
            run = run + w if w > 0 else 0
            best = max(best, run)
        return best
