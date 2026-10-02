class Solution:
    # Mistake: returns 1 for exp 0 even when mod is 1.
    def powerMod(self, base, exp, mod):
        b, r = base % mod, 1
        while exp:
            if exp & 1:
                r = r * b % mod
            b = b * b % mod
            exp >>= 1
        return r
