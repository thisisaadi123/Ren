import bisect
class Solution:
    # Mistake: counts prices[i] >= 2 * prices[j].
    def countBigDrops(self, prices):
        total = 0
        s = []
        for x in reversed(prices):
            total += bisect.bisect_right(s, x / 2)
            bisect.insort(s, x)
        return total
