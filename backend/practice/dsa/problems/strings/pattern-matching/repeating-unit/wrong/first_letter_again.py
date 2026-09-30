class Solution:
    # Mistake: only tries the block that ends where the first letter comes back.
    def shortestUnit(self, s):
        n = len(s)
        p = s.find(s[0], 1)
        if p > 0 and n % p == 0 and s[:p] * (n // p) == s:
            return p
        return n
