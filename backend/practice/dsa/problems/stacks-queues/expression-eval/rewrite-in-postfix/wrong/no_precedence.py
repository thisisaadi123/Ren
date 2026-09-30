class Solution:
    # Mistake: ignores precedence and applies operators strictly left to right.
    def toPostfix(self, expr):
        out, ops = [], []
        for c in expr:
            if c == "(":
                ops.append(c)
            elif c == ")":
                while ops[-1] != "(":
                    out.append(ops.pop())
                ops.pop()
            elif c in "+-*/^":
                while ops and ops[-1] != "(":
                    out.append(ops.pop())
                ops.append(c)
            else:
                out.append(c)
        while ops:
            out.append(ops.pop())
        return "".join(out)
