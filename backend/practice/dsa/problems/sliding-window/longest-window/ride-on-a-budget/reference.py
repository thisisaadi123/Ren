class Solution:
    def longestRide(self, fares, budget):
        left = total = best = 0
        for i, f in enumerate(fares):
            total += f
            while total > budget:
                total -= fares[left]
                left += 1
            best = max(best, i - left + 1)
        return best
