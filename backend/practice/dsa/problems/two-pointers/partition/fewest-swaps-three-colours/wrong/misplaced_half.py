class Solution:
    # Mistake: assumes every swap fixes two balls.
    def minSwapsThreeColours(self, balls):
        s = sorted(balls)
        wrong = sum(1 for a, b in zip(balls, s) if a != b)
        return (wrong + 1) // 2
