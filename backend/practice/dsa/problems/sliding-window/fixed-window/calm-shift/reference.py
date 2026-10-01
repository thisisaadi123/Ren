class Solution:
    def mostServed(self, customers, moody, minutes):
        base = sum(c for c, m in zip(customers, moody) if not m)
        gain = sum(customers[i] * moody[i] for i in range(minutes))
        best = gain
        for i in range(minutes, len(customers)):
            gain += customers[i] * moody[i] - customers[i - minutes] * moody[i - minutes]
            best = max(best, gain)
        return base + best
