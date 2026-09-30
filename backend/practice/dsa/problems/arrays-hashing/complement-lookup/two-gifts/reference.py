class Solution:
    def pickTwo(self, prices, budget):
        where = {}
        for j, p in enumerate(prices):
            if budget - p in where:
                return [where[budget - p], j]
            where[p] = j
