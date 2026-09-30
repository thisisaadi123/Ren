class Solution:
    def evalPostfix(self, tokens):
        pos = [len(tokens) - 1]
        def node():
            t = tokens[pos[0]]
            pos[0] -= 1
            if t in ("+", "-", "*", "/"):
                b = node()
                a = node()
                return {"+": a + b, "-": a - b, "*": a * b}.get(t) if t != "/" else int(a / b)
            return int(t)
        return node()
