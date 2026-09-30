class Solution:
    def longestEchoText(self, s):
        n = len(s)
        best = s[0]
        for c in range(n):
            i = j = c
            while i >= 0 and j < n and s[i] == s[j]:
                i -= 1
                j += 1
            if j - i - 1 > len(best):
                best = s[i + 1:j]
        return best
