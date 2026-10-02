class Solution:
    # Mistake: forgets the extra factor when the exponent is odd.
    def powerMod(self, base, exp, mod):
        b = base % mod

        def go(e):
            if e == 0:
                return 1 % mod
            if e == 1:
                return b
            h = go(e // 2)
            return h * h % mod
        return go(exp)
