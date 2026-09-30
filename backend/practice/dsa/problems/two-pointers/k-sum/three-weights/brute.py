import itertools
class Solution:
    def hasTriple(self, weights, target):
        return any(sum(c) == target for c in itertools.combinations(weights, 3))
