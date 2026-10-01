class Solution:
    # Mistake: treats spending the whole budget as going over.
    def longestRide(self, fares, budget):
        left = total = best = 0
        for i, f in enumerate(fares):
            total += f
            while total >= budget and left <= i:
                total -= fares[left]
                left += 1
            best = max(best, i - left + 1)
        return best
