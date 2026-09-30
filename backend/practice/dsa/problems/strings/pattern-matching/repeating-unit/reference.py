class Solution:
    def shortestUnit(self, s):
        n = len(s)
        fail = [0] * n
        k = 0
        for i in range(1, n):
            while k and s[i] != s[k]:
                k = fail[k - 1]
            if s[i] == s[k]:
                k += 1
            fail[i] = k
        p = n - fail[-1]
        return p if n % p == 0 else n
