class Solution:
    # Mistake: when too many `(` remain, removes the earliest ones instead of the unmatched ones.
    def stripStray(self, s):
        out, d = [], 0
        for c in s:
            if c == ")":
                if d == 0:
                    continue
                d -= 1
            elif c == "(":
                d += 1
            out.append(c)
        res = []
        for c in out:
            if c == "(" and d > 0:
                d -= 1
                continue
            res.append(c)
        return "".join(res)
