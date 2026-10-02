class Solution:
    def fewestTrips(self, boxes, capacity):
        n = len(boxes)
        full = (1 << n) - 1
        fits = [sum(boxes[i] for i in range(n) if m >> i & 1) <= capacity for m in range(1 << n)]
        INF = n + 1
        dp = [INF] * (1 << n)
        dp[0] = 0
        for m in range(1, 1 << n):
            low = m & -m
            sub = m
            while sub:
                if sub & low and fits[sub]:
                    dp[m] = min(dp[m], dp[m ^ sub] + 1)
                sub = (sub - 1) & m
        return dp[full]
