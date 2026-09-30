import re
from ren_check import text
def validate(expr):
    text("expr", expr, 1, 10**5, "0123456789+-*/() ")
    assert not re.search(r"\d +\d", expr), "a space may not split a number, and two numbers need an operator between them"
    toks = re.findall(r"\d+|[-+*/()]", expr)
    want, depth, prev = True, 0, None
    for t in toks:
        if want:
            if t.isdigit():
                want = False
            elif t == "(":
                depth += 1
            else:
                assert t == "-" and prev in (None, "("), "expr must be valid: a sign - may only appear at the start or right after ("
        else:
            if t == ")":
                assert depth > 0, "parentheses must be balanced"
                depth -= 1
            else:
                assert t in "+-*/", "expr must be valid: an operator or ) was expected after a number"
                want = True
        prev = t
    assert not want, "expr must not end with an operator, and parentheses may not be empty"
    assert depth == 0, "parentheses must be balanced"
    LO, HI = -2**31, 2**31 - 1
    def fit(v):
        assert LO <= v <= HI, "every number and intermediate result fits in a signed 32-bit integer"
    def total(st):
        s = 0
        for x in st:
            s += x
            fit(s)
        return s
    frames, st, op, num = [], [], "+", None
    for t in toks + ["#"]:
        if t.isdigit():
            num = int(t)
            fit(num)
            continue
        if t == "(":
            frames.append((st, op))
            st, op, num = [], "+", None
            continue
        if num is None:
            num = 0
        if op == "+":
            st.append(num)
        elif op == "-":
            st.append(-num)
        elif op == "*":
            st[-1] *= num
        else:
            assert num != 0, "no division by zero"
            q = abs(st[-1]) // abs(num)
            st[-1] = q if (st[-1] < 0) == (num < 0) else -q
        fit(st[-1])
        if t == ")":
            num = total(st)
            st, op = frames.pop()
        else:
            op, num = t, None
    total(st)
