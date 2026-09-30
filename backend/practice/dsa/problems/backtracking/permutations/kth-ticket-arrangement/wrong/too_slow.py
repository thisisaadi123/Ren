import itertools
class Solution:
    # Walks through the orders one by one until the k-th: up to 18! steps.
    def kthArrangement(self, n, k):
        for i, p in enumerate(itertools.permutations(range(1, n + 1)), 1):
            if i == k:
                return list(p)
