class Solution:
    # Walks every streak from every day, not just from streak starts: O(n^2) on one long streak.
    def longestStreak(self, days):
        have = set(days)
        best = 0
        for d in days:
            end = d
            while end + 1 in have:
                end += 1
            best = max(best, end - d + 1)
        return best
