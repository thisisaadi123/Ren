class Solution:
    def longestEchoText(self, s):
        n = len(s)
        best = s[0]
        for L in range(n, 0, -1):
            for i in range(n - L + 1):
                t = s[i:i + L]
                if t == t[::-1]:
                    return t
        return best
