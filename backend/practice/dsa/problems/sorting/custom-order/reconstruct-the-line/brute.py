import itertools
class Solution:
    def rebuildLine(self, people):
        for perm in itertools.permutations(people):
            if all(sum(1 for q in perm[:i] if q[0] >= p[0]) == p[1] for i, p in enumerate(perm)):
                return [list(p) for p in perm]
