class Solution:
    def countPairsWithin(self, mains, sides, budget):
        total = 0
        for x in mains:
            for y in sides:
                if x + y <= budget:
                    total += 1
        return total
