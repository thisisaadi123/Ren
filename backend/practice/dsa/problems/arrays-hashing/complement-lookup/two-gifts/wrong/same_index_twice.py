class Solution:
    # Mistake: stores the price before looking up, so one gift can pair with itself.
    def pickTwo(self, prices, budget):
        where = {}
        for j, p in enumerate(prices):
            where.setdefault(p, j)
            if budget - p in where:
                return [where[budget - p], j]
