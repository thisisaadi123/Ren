from ren_check import text
def validate(s):
    text("s", s, 2, 10**5, "()")
    d = 0
    for c in s:
        d += 1 if c == "(" else -1
        assert d >= 0, "s must be balanced"
    assert d == 0, "s must be balanced"
