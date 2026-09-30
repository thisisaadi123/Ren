class Solution:
    # Mistake: counts misplaced balls.
    def minSwapsThreeColours(self, balls):
        return sum(1 for a, b in zip(balls, sorted(balls)) if a != b)
