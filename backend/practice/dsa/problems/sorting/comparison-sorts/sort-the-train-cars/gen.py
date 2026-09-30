from ren_gen import ints
def small(rng):
    return {"head": ints(rng, rng.randint(0, 7), -5, 5)}
def build(rng, n, lo=-10**5, hi=10**5, shape="random"):
    a = ints(rng, n, lo, hi)
    if shape == "reversed":
        a.sort(reverse=True)
    return {"head": a}
