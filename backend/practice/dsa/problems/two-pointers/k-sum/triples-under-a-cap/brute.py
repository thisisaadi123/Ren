import itertools
class Solution:
    def countTriplesBelow(self, values, cap):
        return sum(1 for c in itertools.combinations(values, 3) if sum(c) < cap)
