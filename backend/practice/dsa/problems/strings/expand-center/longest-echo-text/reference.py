class Solution:
    def longestEchoText(self, s):
        n = len(s)
        best_i, best_len = 0, 1
        for c in range(2 * n - 1):
            i, j = c // 2, c // 2 + c % 2
            while i >= 0 and j < n and s[i] == s[j]:
                i -= 1
                j += 1
            length = j - i - 1
            start = i + 1
            if length > best_len or (length == best_len and start < best_i):
                best_i, best_len = start, length
        return s[best_i:best_i + best_len]
