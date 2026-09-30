class Solution:
    # Mistake: finds the largest clear square, not the largest rectangle.
    def largestClearPlot(self, land):
        R, C = len(land), len(land[0])
        dp = [[0] * (C + 1) for _ in range(R + 1)]
        best = 0
        for r in range(R):
            for c in range(C):
                if land[r][c] == "1":
                    dp[r + 1][c + 1] = 1 + min(dp[r][c], dp[r][c + 1], dp[r + 1][c])
                    best = max(best, dp[r + 1][c + 1])
        return best * best
