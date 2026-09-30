class Solution:
    def countTriplesInBand(self, values, low, high):
        n = len(values)
        total = 0
        for i in range(n):
            for j in range(i + 1, n):
                for k in range(j + 1, n):
                    if low <= values[i] + values[j] + values[k] <= high:
                        total += 1
        return total
