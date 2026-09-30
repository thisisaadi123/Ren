class Solution:
    # Mistake: removes the unmatched `)` but keeps the `(` that are never closed.
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
        return "".join(out)
