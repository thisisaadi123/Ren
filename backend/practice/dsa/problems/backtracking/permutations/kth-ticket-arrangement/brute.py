import itertools
class Solution:
    def kthArrangement(self, n, k):
        for i, p in enumerate(itertools.permutations(range(1, n + 1)), 1):
            if i == k:
                return list(p)
