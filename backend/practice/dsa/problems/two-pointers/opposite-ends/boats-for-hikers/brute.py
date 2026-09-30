import functools
class Solution:
    def fewestBoats(self, weights, limit):
        n = len(weights)
        @functools.lru_cache(None)
        def go(mask):
            if mask == 0:
                return 0
            i = (mask & -mask).bit_length() - 1
            rest = mask & ~(1 << i)
            best = 1 + go(rest)
            for j in range(n):
                if rest >> j & 1 and weights[i] + weights[j] <= limit:
                    best = min(best, 1 + go(rest & ~(1 << j)))
            return best
        return go((1 << n) - 1)
