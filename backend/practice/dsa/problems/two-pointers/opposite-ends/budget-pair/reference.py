class Solution:
    def budgetPair(self, prices, budget):
        i, j = 0, len(prices) - 1
        while i < j:
            s = prices[i] + prices[j]
            if s == budget:
                return [i, j]
            if s < budget:
                i += 1
            else:
                j -= 1
        return [-1, -1]
