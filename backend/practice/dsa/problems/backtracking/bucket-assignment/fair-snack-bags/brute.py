from itertools import product


class Solution:
    def fairestSplit(self, bags, kids):
        best = sum(bags)
        for who in product(range(kids), repeat=len(bags)):
            load = [0] * kids
            for b, w in zip(bags, who):
                load[w] += b
            best = min(best, max(load))
        return best
