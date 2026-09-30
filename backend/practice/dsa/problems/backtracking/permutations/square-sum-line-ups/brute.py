import itertools, math
class Solution:
    def squareLineUps(self, nums):
        good = set()
        for p in itertools.permutations(nums):
            if all(math.isqrt(a + b) ** 2 == a + b for a, b in zip(p, p[1:])):
                good.add(p)
        return len(good)
