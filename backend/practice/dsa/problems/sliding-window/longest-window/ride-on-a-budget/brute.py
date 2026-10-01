class Solution:
    def longestRide(self, fares, budget):
        n = len(fares)
        best = 0
        for i in range(n):
            for j in range(i, n):
                if sum(fares[i:j + 1]) <= budget:
                    best = max(best, j - i + 1)
        return best
