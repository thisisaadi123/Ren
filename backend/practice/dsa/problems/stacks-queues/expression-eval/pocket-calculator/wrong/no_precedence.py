class Solution:
    # Mistake: handles parentheses but applies + - * / strictly left to right inside them.
    def evaluate(self, expr):
        def apply(a, op, b):
            if op == "+":
                return a + b
            if op == "-":
                return a - b
            if op == "*":
                return a * b
            q = abs(a) // abs(b)
            return q if (a < 0) == (b < 0) else -q
        frames = []
        val, op, num = 0, "+", 0
        for c in expr + "#":
            if c == " ":
                continue
            if c.isdigit():
                num = num * 10 + ord(c) - 48
                continue
            if c == "(":
                frames.append((val, op))
                val, op, num = 0, "+", 0
                continue
            val = apply(val, op, num)
            if c == ")":
                num = val
                val, op = frames.pop()
            else:
                op, num = c, 0
        return val
