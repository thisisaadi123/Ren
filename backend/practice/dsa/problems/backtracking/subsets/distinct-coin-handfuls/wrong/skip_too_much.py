class Solution:
    # Mistake: skips a repeated value even as the first choice at a depth (i > 0 instead of i > start),
    # so handfuls with two equal coins like [2, 2] are lost.
    def coinHandfuls(self, coins):
        c = sorted(coins)
        out, pick = [], []
        def go(start):
            out.append(pick[:])
            for i in range(start, len(c)):
                if i > 0 and c[i] == c[i - 1]:
                    continue
                pick.append(c[i])
                go(i + 1)
                pick.pop()
        go(0)
        return out
