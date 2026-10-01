class Solution:
    # Mistake: counts a repeat when it enters but never clears it when it leaves.
    def bestUniqueBundle(self, prices, k):
        count = {}
        dup = total = best = 0
        for i, v in enumerate(prices):
            count[v] = count.get(v, 0) + 1
            if count[v] == 2:
                dup += 1
            total += v
            if i >= k:
                w = prices[i - k]
                count[w] -= 1
                total -= w
            if i >= k - 1 and dup == 0:
                best = max(best, total)
        return best
