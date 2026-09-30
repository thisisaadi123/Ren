class Solution:
    def coinHandfuls(self, coins):
        c = sorted(coins)
        out, pick = [], []

        def go(start):
            out.append(pick[:])
            for i in range(start, len(c)):
                if i > start and c[i] == c[i - 1]:
                    continue
                pick.append(c[i])
                go(i + 1)
                pick.pop()

        go(0)
        return sorted(out)
