class Solution:
    def hasLowHighBetween(self, values):
        n = len(values)
        return any(values[i] < values[k] < values[j]
                   for i in range(n) for j in range(i + 1, n) for k in range(j + 1, n))
