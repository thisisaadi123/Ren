class Solution:
    # Mistake: returns only the customers saved by the calm stretch.
    def mostServed(self, customers, moody, minutes):
        gain = sum(customers[i] * moody[i] for i in range(minutes))
        best = gain
        for i in range(minutes, len(customers)):
            gain += customers[i] * moody[i] - customers[i - minutes] * moody[i - minutes]
            best = max(best, gain)
        return best
