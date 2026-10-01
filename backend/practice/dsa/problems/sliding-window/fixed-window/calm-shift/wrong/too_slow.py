class Solution:
    # Mistake: re-adds every window: O(n * minutes).
    def mostServed(self, customers, moody, minutes):
        base = sum(c for c, m in zip(customers, moody) if not m)
        best = 0
        for s in range(len(customers) - minutes + 1):
            g = 0
            for i in range(s, s + minutes):
                g += customers[i] * moody[i]
            best = max(best, g)
        return base + best
