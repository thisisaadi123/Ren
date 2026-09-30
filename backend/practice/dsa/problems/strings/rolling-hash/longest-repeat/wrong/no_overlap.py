class Solution:
    # Mistake: requires the two copies not to overlap.
    def longestRepeat(self, s):
        n = len(s)
        for L in range(n // 2, 0, -1):
            first = {}
            for i in range(n - L + 1):
                t = s[i:i + L]
                if t in first and first[t] + L <= i:
                    return L
                first.setdefault(t, i)
        return 0
