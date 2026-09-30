class Solution:
    def longestEcho(self, s):
        n = len(s)
        best = 1
        for c in range(2 * n - 1):
            i, j = c // 2, c // 2 + c % 2
            while i >= 0 and j < n and s[i] == s[j]:
                i -= 1
                j += 1
            best = max(best, j - i - 1)
        return best
