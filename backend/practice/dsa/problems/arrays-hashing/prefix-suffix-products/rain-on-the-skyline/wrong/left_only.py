class Solution:
    # Mistake: only looks at the tallest wall on the left.
    def trappedWater(self, walls):
        total = best = 0
        for w in walls:
            best = max(best, w)
            total += best - w
        return total
