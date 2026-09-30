class Solution:
    def rangeTotals(self, sales, queries):
        return [sum(sales[l : r + 1]) for l, r in queries]
