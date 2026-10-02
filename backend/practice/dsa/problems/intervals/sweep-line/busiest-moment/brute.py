class Solution:
    def busiestMoment(self, visits):
        best, at = -1, None
        for t in sorted({s for s, _ in visits}):
            c = sum(1 for s, e in visits if s <= t <= e)
            if c > best:
                best, at = c, t
        return at
