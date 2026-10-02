class Solution:
    def powerMod(self, base, exp, mod):
        b = base % mod

        def go(e):
            if e == 0:
                return 1 % mod
            h = go(e // 2)
            h = h * h % mod
            return h * b % mod if e % 2 else h
        return go(exp)
