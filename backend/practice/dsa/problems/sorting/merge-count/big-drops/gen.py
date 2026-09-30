from ren_gen import ints
def small(rng):
    return {"prices": ints(rng, rng.randint(1, 8), -8, 8)}
def build(rng, n, lo=-2**31, hi=2**31 - 1, shape="random"):
    a = ints(rng, n, lo, hi)
    if shape == "reversed":
        a.sort(reverse=True)
    return {"prices": a}
