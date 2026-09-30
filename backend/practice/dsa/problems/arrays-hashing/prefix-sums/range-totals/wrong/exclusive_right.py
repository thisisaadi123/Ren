class Solution:
    # Mistake: treats r as exclusive.
    def rangeTotals(self, sales, queries):
        prefix = [0]
        for s in sales:
            prefix.append(prefix[-1] + s)
        return [prefix[r] - prefix[l] for l, r in queries]
