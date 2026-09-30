class Solution:
    # Mistake: repeatedly searches from the left for the next * or / and rebuilds the token list: O(n²).
    def calculate(self, expr):
        toks, num = [], ""
        for c in expr:
            if c.isdigit():
                num += c
            elif c != " ":
                toks += [int(num), c]
                num = ""
        toks.append(int(num))
        while True:
            i = 1
            while i < len(toks) and toks[i] not in ("*", "/"):
                i += 2
            if i >= len(toks):
                break
            a, b = toks[i - 1], toks[i + 1]
            toks = toks[:i - 1] + [a * b if toks[i] == "*" else a // b] + toks[i + 2:]
        total = toks[0]
        for i in range(1, len(toks), 2):
            total = total + toks[i + 1] if toks[i] == "+" else total - toks[i + 1]
        return total
