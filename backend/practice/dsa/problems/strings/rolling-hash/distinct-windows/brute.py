class Solution:
    def distinctWindows(self, s, k):
        return len({s[i:i + k] for i in range(len(s) - k + 1)})
