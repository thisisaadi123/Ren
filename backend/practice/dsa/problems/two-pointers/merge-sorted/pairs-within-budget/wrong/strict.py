class Solution:
    # Mistake: requires the total to be strictly under budget.
    def countPairsWithin(self, mains, sides, budget):
        total = 0
        j = len(sides) - 1
        for x in mains:
            while j >= 0 and x + sides[j] >= budget:
                j -= 1
            total += j + 1
        return total
