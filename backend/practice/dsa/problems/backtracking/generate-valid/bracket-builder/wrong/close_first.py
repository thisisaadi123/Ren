class Solution:
    # Mistake: tries ')' before '(' so the order is reversed.
    def buildBrackets(self, n):
        out = []

        def go(s, op, cl):
            if len(s) == 2 * n:
                out.append(s)
                return
            if cl < op:
                go(s + ")", op, cl + 1)
            if op < n:
                go(s + "(", op + 1, cl)

        go("", 0, 0)
        return out
