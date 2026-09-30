class Solution:
    def toPostfix(self, expr):
        pos = [0]
        def peek():
            return expr[pos[0]] if pos[0] < len(expr) else ""
        def take():
            pos[0] += 1
            return expr[pos[0] - 1]
        def atom():
            if peek() == "(":
                take()
                r = add()
                take()
                return r
            return take()
        def power():
            base = atom()
            if peek() == "^":
                take()
                return base + power() + "^"
            return base
        def mul():
            r = power()
            while peek() in ("*", "/"):
                op = take()
                r = r + power() + op
            return r
        def add():
            r = mul()
            while peek() in ("+", "-"):
                op = take()
                r = r + mul() + op
            return r
        return add()
