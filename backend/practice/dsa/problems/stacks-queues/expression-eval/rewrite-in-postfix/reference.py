class Solution:
    def toPostfix(self, expr):
        prec = {"+": 1, "-": 1, "*": 2, "/": 2, "^": 3}
        out, ops = [], []
        for c in expr:
            if c == "(":
                ops.append(c)
            elif c == ")":
                while ops[-1] != "(":
                    out.append(ops.pop())
                ops.pop()
            elif c in prec:
                while ops and ops[-1] != "(" and (prec[ops[-1]] > prec[c] or (prec[ops[-1]] == prec[c] and c != "^")):
                    out.append(ops.pop())
                ops.append(c)
            else:
                out.append(c)
        while ops:
            out.append(ops.pop())
        return "".join(out)
