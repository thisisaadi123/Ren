from collections import Counter


class Solution:
    def shortestFix(self, s):
        n = len(s)
        q = n // 4
        for length in range(0, n + 1):
            for i in range(n - length + 1):
                rest = Counter(s[:i] + s[i + length:])
                if all(rest[c] <= q for c in "SATB"):
                    return length
        return n
