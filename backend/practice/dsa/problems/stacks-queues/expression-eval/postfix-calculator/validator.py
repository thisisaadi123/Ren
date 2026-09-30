import re
def validate(tokens):
    assert isinstance(tokens, list) and 1 <= len(tokens) <= 10**5, "tokens must have 1 to 10^5 items"
    st = []
    for t in tokens:
        assert isinstance(t, str), "every token is a string"
        if t in ("+", "-", "*", "/"):
            assert len(st) >= 2, "every operator needs two values before it"
            b, a = st.pop(), st.pop()
            if t == "/":
                assert b != 0, "no division by zero"
                q = abs(a) // abs(b)
                r = q if (a < 0) == (b < 0) else -q
            else:
                r = a + b if t == "+" else a - b if t == "-" else a * b
            assert -2**31 <= r <= 2**31 - 1, "every intermediate result fits in a signed 32-bit integer"
            st.append(r)
        else:
            assert re.fullmatch(r"-?(0|[1-9][0-9]*)", t) and t != "-0", "numbers are integers without leading zeros"
            assert -200 <= int(t) <= 200, "numbers are between -200 and 200"
            st.append(int(t))
    assert len(st) == 1, "the tokens form one complete postfix expression"
