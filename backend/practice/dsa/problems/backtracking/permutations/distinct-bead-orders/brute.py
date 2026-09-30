import itertools
class Solution:
    def beadOrders(self, beads):
        return [list(p) for p in set(itertools.permutations(beads))]
