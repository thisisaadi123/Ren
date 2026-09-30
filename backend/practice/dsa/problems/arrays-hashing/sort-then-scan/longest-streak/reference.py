class Solution:
    def longestStreak(self, days):
        have = set(days)
        best = 0
        for d in have:
            if d - 1 not in have:
                end = d
                while end + 1 in have:
                    end += 1
                best = max(best, end - d + 1)
        return best
