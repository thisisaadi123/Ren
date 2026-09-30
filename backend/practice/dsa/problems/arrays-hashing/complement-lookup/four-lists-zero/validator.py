from ren_check import ints
def validate(a, b, c, d):
    lim = 2**28
    ints("a", a, 1, 500, -lim, lim)
    for name, lst in (("b", b), ("c", c), ("d", d)):
        ints(name, lst, len(a), len(a), -lim, lim)
