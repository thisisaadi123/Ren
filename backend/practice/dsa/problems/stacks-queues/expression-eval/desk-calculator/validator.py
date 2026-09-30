import re
from ren_check import text
def validate(expr):
    text("expr", expr, 1, 10**5, "0123456789+-*/ ")
    toks = re.findall(r"\d+|[-+*/]| +", expr)
    toks = [t for t in toks if not t.startswith(" ")]
    squashed = re.sub(r"(?<=\d) +(?=\d)", "|", expr)
    assert "|" not in squashed, "a space may not split a number, and two numbers need an operator between them"
    assert toks and len(toks) % 2 == 1, "expr must be a valid expression"
    for i, t in enumerate(toks):
        if i % 2 == 0:
            assert t.isdigit(), "numbers and operators must alternate, starting and ending with a number"
        else:
            assert t in "+-*/", "numbers and operators must alternate, starting and ending with a number"
    LO, HI = -2**31, 2**31 - 1
    fits = lambda v: LO <= v <= HI
    total, term, sign = 0, int(toks[0]), 1
    assert fits(term), "every number fits in a signed 32-bit integer"
    for i in range(1, len(toks), 2):
        op, v = toks[i], int(toks[i + 1])
        assert fits(v), "every number fits in a signed 32-bit integer"
        if op == "*":
            term *= v
        elif op == "/":
            assert v != 0, "no division by zero"
            term //= v
        else:
            total += sign * term
            assert fits(total), "every intermediate result fits in a signed 32-bit integer"
            term, sign = v, (1 if op == "+" else -1)
        assert fits(term), "every intermediate result fits in a signed 32-bit integer"
    total += sign * term
    assert fits(total), "the answer fits in a signed 32-bit integer"
