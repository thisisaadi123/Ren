class Solution:
    def shortestUnit(self, s):
        n = len(s)
        for p in range(1, n + 1):
            if n % p == 0 and s[:p] * (n // p) == s:
                return p
