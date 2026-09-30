class Solution:
    # Mistake: returns positions starting at 1.
    def budgetPair(self, prices, budget):
        i, j = 0, len(prices) - 1
        while i < j:
            s = prices[i] + prices[j]
            if s == budget:
                return [i + 1, j + 1]
            if s < budget:
                i += 1
            else:
                j -= 1
