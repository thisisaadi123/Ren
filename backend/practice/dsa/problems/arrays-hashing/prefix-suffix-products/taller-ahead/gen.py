from ren_gen import ints
def small(rng):
    return {"heights": ints(rng, rng.randint(1, 8), 1, 9)}
def build(rng, n, lo=1, hi=10**9, shape="random"):
    h = ints(rng, n, lo, hi)
    if shape == "increasing":
        h.sort()
    elif shape == "decreasing":
        h.sort(reverse=True)
    return {"heights": h}
