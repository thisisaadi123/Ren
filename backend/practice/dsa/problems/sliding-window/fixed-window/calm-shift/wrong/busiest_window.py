class Solution:
    # Mistake: calms the window with the most customers overall, not the most unhappy ones.
    def mostServed(self, customers, moody, minutes):
        base = sum(c for c, m in zip(customers, moody) if not m)
        window = sum(customers[:minutes])
        best, at = window, 0
        for i in range(minutes, len(customers)):
            window += customers[i] - customers[i - minutes]
            if window > best:
                best, at = window, i - minutes + 1
        return base + sum(customers[i] * moody[i] for i in range(at, at + minutes))
