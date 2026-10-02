class Solution:
    def buildBrackets(self, n):
        out, cur = [], []

        def go(op, cl):
            if len(cur) == 2 * n:
                out.append("".join(cur))
                return
            if op < n:
                cur.append("(")
                go(op + 1, cl)
                cur.pop()
            if cl < op:
                cur.append(")")
                go(op, cl + 1)
                cur.pop()

        go(0, 0)
        return out
