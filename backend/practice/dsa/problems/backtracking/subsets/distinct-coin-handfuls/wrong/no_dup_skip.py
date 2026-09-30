class Solution:
    # Mistake: never skips equal values, so the same handful is listed several times.
    def coinHandfuls(self, coins):
        c = sorted(coins)
        out, pick = [], []
        def go(start):
            out.append(pick[:])
            for i in range(start, len(c)):
                pick.append(c[i])
                go(i + 1)
                pick.pop()
        go(0)
        return out
