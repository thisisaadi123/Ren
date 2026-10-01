class Solution:
    # Mistake: extends from every start: O(n^2) when the budget is large.
    def longestRide(self, fares, budget):
        n = len(fares)
        best = 0
        for i in range(n):
            t = 0
            for j in range(i, n):
                t += fares[j]
                if t > budget:
                    break
                best = max(best, j - i + 1)
        return best
