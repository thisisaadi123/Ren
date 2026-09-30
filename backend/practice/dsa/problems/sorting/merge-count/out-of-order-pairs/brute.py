import itertools
class Solution:
    def countOutOfOrder(self, ranks):
        return sum(1 for a, b in itertools.combinations(ranks, 2) if a > b)
