class Solution:
    def longestEcho(self, s):
        n = len(s)
        return max(j - i for i in range(n) for j in range(i + 1, n + 1) if s[i:j] == s[i:j][::-1])
