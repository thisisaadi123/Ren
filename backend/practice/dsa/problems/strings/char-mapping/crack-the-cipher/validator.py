from ren_check import text
def validate(plain, coded, message):
    alpha = "abcdefghijklmnopqrstuvwxyz "
    text("plain", plain, 1, 10**5, alpha)
    text("coded", coded, len(plain), len(plain), alpha)
    text("message", message, 1, 10**5, alpha)
    fwd, back = {}, {}
    for p, c in zip(plain, coded):
        assert (p == " ") == (c == " "), "plain and coded have spaces in the same places"
        if p != " ":
            assert fwd.setdefault(p, c) == c and back.setdefault(c, p) == p, "plain and coded must agree with a one-to-one substitution"
