class Solution:
    # Mistake: trusts floating point; near 10^15 neighbours of a square pass as squares.
    def isPerfectSquare(self, tiles):
        r = tiles ** 0.5
        return abs(r - round(r)) < 1e-6
