import itertools
class Solution:
    def nextArrangement(self, values):
        perms = sorted(set(itertools.permutations(values)))
        i = perms.index(tuple(values))
        return list(perms[(i + 1) % len(perms)])
