class Solution:
    # Mistake: floating-point rounding goes wrong just below perfect squares.
    def squareFloor(self, x):
        return int(x ** 0.5 + 0.5)
