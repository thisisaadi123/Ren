class Solution:
    # Mistake: floating-point formula; near huge triangle numbers it's off by one.
    def rowsNeeded(self, cans):
        return int(((8 * cans + 1) ** 0.5 - 1) / 2 + 0.999999)
