class Solution:
    def bestWeek(self, sales, k):
        return max(sum(sales[i:i + k]) for i in range(len(sales) - k + 1))
