class Solution:
    def longestOnline(self, status, k):
        n = len(status)
        best = 0
        for i in range(n):
            for j in range(i, n):
                if status[i:j + 1].count(0) <= k:
                    best = max(best, j - i + 1)
        return best
