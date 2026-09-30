class Solution:
    # Mistake: forgets that the unit must divide the length ("abcab" has no unit of 3).
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
        return n - fail[-1]
