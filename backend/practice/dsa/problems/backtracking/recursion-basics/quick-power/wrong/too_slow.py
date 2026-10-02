class Solution:
    # Mistake: multiplies exp times.
    def powerMod(self, base, exp, mod):
        r = 1 % mod
        for _ in range(exp):
            r = r * base % mod
        return r
