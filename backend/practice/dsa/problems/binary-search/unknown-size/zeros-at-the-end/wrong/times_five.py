class Solution:
    # Mistake: assumes every multiple of 5 adds exactly one zero (forgets 25, 125, ...).
    def smallestWithZeros(self, zeros):
        return 5 * zeros
