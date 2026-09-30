class Solution:
    def longestStreak(self, days):
        best = 0
        for d in days:
            k = 0
            while d + k in days:
                k += 1
            best = max(best, k)
        return best
