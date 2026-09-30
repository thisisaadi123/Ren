import re
class Solution:
    def evaluate(self, expr):
        toks = re.findall(r"\d+|[-+*/()]", expr)
        pos = [0]
        def peek():
            return toks[pos[0]] if pos[0] < len(toks) else ""
        def take():
            pos[0] += 1
            return toks[pos[0] - 1]
        def factor():
            if peek() == "(":
                take()
                v = add()
                take()
                return v
            return int(take())
        def mul():
            v = factor()
            while peek() in ("*", "/"):
                op, w = take(), factor()
                v = v * w if op == "*" else int(v / w)
            return v
        def add():
            neg = peek() == "-"
            if neg:
                take()
            v = mul()
            if neg:
                v = -v
            while peek() in ("+", "-"):
                op, w = take(), mul()
                v = v + w if op == "+" else v - w
            return v
        return add()
