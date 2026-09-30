import itertools
class Solution:
    def countTriplesInBand(self, values, low, high):
        return sum(1 for c in itertools.combinations(values, 3) if low <= sum(c) <= high)
