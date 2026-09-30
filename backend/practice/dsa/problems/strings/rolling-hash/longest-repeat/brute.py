class Solution:
    def longestRepeat(self, s):
        n = len(s)
        for L in range(n - 1, 0, -1):
            seen = set()
            for i in range(n - L + 1):
                t = s[i:i + L]
                if t in seen:
                    return L
                seen.add(t)
        return 0
