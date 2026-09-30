import itertools
class Solution:
    # Mistake: returns the larger sum on ties.
    def closestTriple(self, values, target):
        return min((sum(c) for c in itertools.combinations(values, 3)), key=lambda s: (abs(s - target), -s))
