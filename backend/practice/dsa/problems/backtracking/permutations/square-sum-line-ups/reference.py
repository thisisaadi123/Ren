class Solution:
    def squareLineUps(self, nums):
        left = collections.Counter(nums)
        vals = sorted(left)
        sq = lambda s: math.isqrt(s) ** 2 == s
        nxt = {v: [w for w in vals if sq(v + w)] for v in vals}
        n = len(nums)

        def go(prev, placed):
            if placed == n:
                return 1
            total = 0
            for w in (vals if prev is None else nxt[prev]):
                if left[w]:
                    left[w] -= 1
                    total += go(w, placed + 1)
                    left[w] += 1
            return total

        return go(None, 0)
