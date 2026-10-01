class Solution:
    # Mistake: when the total goes over, starts a fresh ride at the current hop.
    def longestRide(self, fares, budget):
        left = total = best = 0
        for i, f in enumerate(fares):
            total += f
            if total > budget:
                left, total = i, f
                if total > budget:
                    left, total = i + 1, 0
            best = max(best, i - left + 1)
        return best
