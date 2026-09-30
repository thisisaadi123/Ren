from ren_check import text
def validate(a, b):
    for name, s in (("a", a), ("b", b)):
        text(name, s, 1, 10**4, "0123456789.")
        for r in s.split("."):
            assert 1 <= len(r) <= 50, "each revision of %s is 1 to 50 digits (no empty revisions)" % name
