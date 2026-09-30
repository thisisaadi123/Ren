import itertools
class Solution:
    def stripStray(self, s):
        def ok(t):
            d = 0
            for c in t:
                d += (c == "(") - (c == ")")
                if d < 0:
                    return False
            return d == 0
        pos = [i for i, c in enumerate(s) if c in "()"]
        for k in range(len(pos) + 1):
            for rem in itertools.combinations(pos, k):
                r = set(rem)
                t = "".join(c for i, c in enumerate(s) if i not in r)
                if ok(t):
                    return t
