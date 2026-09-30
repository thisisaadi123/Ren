class Solution:
    def countTriplesBelow(self, values, cap):
        n = len(values)
        return sum(1 for i in range(n) for j in range(i + 1, n) for k in range(j + 1, n) if values[i] + values[j] + values[k] < cap)
