class Solution:
    # Mistake: splits at the loosest top-level operator and recurses, rescanning each piece: O(n²).
    def toPostfix(self, expr):
        prec = {"+": 1, "-": 1, "*": 2, "/": 2, "^": 3}
        def match(s, i):
            d = 0
            for j in range(i, len(s)):
                d += (s[j] == "(") - (s[j] == ")")
                if d == 0:
                    return j
        def conv(s):
            while s[0] == "(" and match(s, 0) == len(s) - 1:
                s = s[1:-1]
            if len(s) == 1:
                return s
            best, where, d = 9, -1, 0
            for i, c in enumerate(s):
                if c == "(":
                    d += 1
                elif c == ")":
                    d -= 1
                elif d == 0 and c in prec:
                    p = prec[c]
                    if p < best or (p == best and p != 3):
                        best, where = p, i
            return conv(s[:where]) + conv(s[where + 1:]) + s[where]
        return conv(expr)
