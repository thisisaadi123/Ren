class Solution:
    # Mistake: only lists squares from 1², so two zeros side by side are rejected.
    def squareLineUps(self, nums):
        left = collections.Counter(nums)
        vals = sorted(left)
        sq = lambda s: s > 0 and math.isqrt(s) ** 2 == s
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
