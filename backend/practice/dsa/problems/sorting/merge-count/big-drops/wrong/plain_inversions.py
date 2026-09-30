class Solution:
    # Mistake: counts every drop, not just the big ones.
    def countBigDrops(self, prices):
        n = len(prices)
        total = 0
        s = []
        import bisect
        for x in reversed(prices):
            total += bisect.bisect_left(s, x)
            bisect.insort(s, x)
        return total
