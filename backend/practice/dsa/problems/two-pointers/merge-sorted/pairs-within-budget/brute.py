class Solution:
    def countPairsWithin(self, mains, sides, budget):
        return sum(1 for x in mains for y in sides if x + y <= budget)
