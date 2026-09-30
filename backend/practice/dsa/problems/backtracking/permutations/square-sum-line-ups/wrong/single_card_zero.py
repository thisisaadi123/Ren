class Solution:
    # Mistake: says a lone card has no neighbours to check and returns 0 instead of 1.
    def squareLineUps(self, nums):
        if len(nums) == 1:
            return 0
        left = collections.Counter(nums)
        vals = sorted(left)
        sq = lambda s: math.isqrt(s) ** 2 == s
        n = len(nums)
        def go(prev, placed):
            if placed == n:
                return 1
            total = 0
            for w in vals:
                if left[w] and (prev is None or sq(prev + w)):
                    left[w] -= 1
                    total += go(w, placed + 1)
                    left[w] += 1
            return total
        return go(None, 0)
