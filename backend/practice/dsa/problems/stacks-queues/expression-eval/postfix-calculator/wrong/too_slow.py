class Solution:
    # Mistake: repeatedly finds the first operator from the left and splices the list: O(n²).
    def evalPostfix(self, tokens):
        toks = list(tokens)
        while len(toks) > 1:
            i = 0
            while toks[i] not in ("+", "-", "*", "/"):
                i += 1
            a, b, t = int(toks[i - 2]), int(toks[i - 1]), toks[i]
            if t == "/":
                q = abs(a) // abs(b)
                r = q if (a < 0) == (b < 0) else -q
            else:
                r = a + b if t == "+" else a - b if t == "-" else a * b
            toks = toks[:i - 2] + [str(r)] + toks[i + 1:]
        return int(toks[0])
