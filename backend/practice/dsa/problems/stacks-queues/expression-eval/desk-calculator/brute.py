import re
class Solution:
    def calculate(self, expr):
        toks = re.findall(r"\d+|[-+*/]", expr)
        vals, ops = [int(toks[0])], []
        for i in range(1, len(toks), 2):
            op, v = toks[i], int(toks[i + 1])
            if op == "*":
                vals[-1] *= v
            elif op == "/":
                vals[-1] = int(vals[-1] / v)
            else:
                ops.append(op)
                vals.append(v)
        total = vals[0]
        for op, v in zip(ops, vals[1:]):
            total = total + v if op == "+" else total - v
        return total
