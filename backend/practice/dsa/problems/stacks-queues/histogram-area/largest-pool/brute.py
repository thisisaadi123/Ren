class Solution:
    def largestPool(self, walls):
        n = len(walls)
        water = [min(max(walls[:i + 1]), max(walls[i:])) - walls[i] for i in range(n)]
        best = run = 0
        for w in water:
            run = run + w if w > 0 else 0
            best = max(best, run)
        return best
