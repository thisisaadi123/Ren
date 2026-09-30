from ren_check import text, integer
def validate(s, t, m):
    integer("m", m, 1, 26)
    alpha = "abcdefghijklmnopqrstuvwxyz"[:m]
    text("s", s, 1, 10**5, alpha)
    text("t", t, len(s), len(s), alpha)
