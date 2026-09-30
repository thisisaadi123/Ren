class Solution:
    # Mistake: sorts but treats a repeated day as breaking the streak.
    def longestStreak(self, days):
        if not days:
            return 0
        s = sorted(days)
        best = run = 1
        for a, b in zip(s, s[1:]):
            run = run + 1 if b == a + 1 else 1
            best = max(best, run)
        return best
