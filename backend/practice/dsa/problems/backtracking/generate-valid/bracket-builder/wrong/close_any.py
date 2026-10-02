class Solution:
    # Mistake: allows ')' whenever there are closings left, even with nothing open.
    def buildBrackets(self, n):
        out = []

        def go(s, op, cl):
            if len(s) == 2 * n:
                out.append(s)
                return
            if op < n:
                go(s + "(", op + 1, cl)
            if cl < n:
                go(s + ")", op, cl + 1)

        go("", 0, 0)
        return out
