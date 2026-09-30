import itertools
class Solution:
    def zeroTriples(self, values):
        found = set(tuple(sorted(c)) for c in itertools.combinations(values, 3) if sum(c) == 0)
        return [list(t) for t in sorted(found)]
