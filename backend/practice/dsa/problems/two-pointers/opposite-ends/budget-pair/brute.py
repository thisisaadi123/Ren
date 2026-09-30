class Solution:
    def budgetPair(self, prices, budget):
        n = len(prices)
        for i in range(n):
            for j in range(i + 1, n):
                if prices[i] + prices[j] == budget:
                    return [i, j]
