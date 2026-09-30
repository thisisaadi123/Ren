class Solution:
    # Mistake: branches over card positions, so swapping two equal cards counts as a new line-up.
    def squareLineUps(self, nums):
        n = len(nums)
        used = [False] * n
        sq = lambda s: math.isqrt(s) ** 2 == s
        def go(prev, placed):
            if placed == n:
                return 1
            total = 0
            for i in range(n):
                if not used[i] and (prev is None or sq(prev + nums[i])):
                    used[i] = True
                    total += go(nums[i], placed + 1)
                    used[i] = False
            return total
        return go(None, 0)
