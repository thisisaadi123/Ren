from itertools import product


class Solution:
    def buildBrackets(self, n):
        out = []
        for t in product("()", repeat=2 * n):
            d = 0
            for c in t:
                d += 1 if c == "(" else -1
                if d < 0:
                    break
            if d == 0:
                out.append("".join(t))
        return sorted(out)
