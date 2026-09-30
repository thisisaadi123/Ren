from ren_check import text
def validate(expr):
    text("expr", expr, 1, 10**5, "abcdefghijklmnopqrstuvwxyz+-*/^()")
    want_operand, depth = True, 0
    for c in expr:
        if want_operand:
            if c == "(":
                depth += 1
            else:
                assert c.isalpha(), "expr must be a valid formula (an operand or ( was expected)"
                want_operand = False
        else:
            if c == ")":
                assert depth > 0, "parentheses must be balanced"
                depth -= 1
            else:
                assert c in "+-*/^", "expr must be a valid formula (an operator or ) was expected)"
                want_operand = True
    assert not want_operand, "expr must not end with an operator"
    assert depth == 0, "parentheses must be balanced"
