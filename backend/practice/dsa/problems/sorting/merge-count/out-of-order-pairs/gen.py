from ren_gen import ints
def small(rng):
    return {"ranks": ints(rng, rng.randint(1, 8), 1, 6)}
def build(rng, n, hi=10**9, shape="random"):
    a = ints(rng, n, 1, hi)
    if shape == "reversed":
        a.sort(reverse=True)
    return {"ranks": a}
