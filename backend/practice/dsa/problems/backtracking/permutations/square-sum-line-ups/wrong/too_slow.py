import itertools, math
class Solution:
    # Tries all n! orders and dedupes the good ones: 12! is about 4.8 × 10^8.
    def squareLineUps(self, nums):
        good = set()
        for p in itertools.permutations(nums):
            if all(math.isqrt(a + b) ** 2 == a + b for a, b in zip(p, p[1:])):
                good.add(p)
        return len(good)
