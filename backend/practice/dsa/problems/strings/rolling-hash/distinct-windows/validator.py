from ren_check import text, integer
def validate(s, k):
    text("s", s, 1, 10**5, "abcdefghijklmnopqrstuvwxyz")
    integer("k", k, 1, len(s))
