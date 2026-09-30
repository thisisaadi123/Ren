from ren_gen import ints
def small(rng):
    return {"scores": ints(rng, rng.randint(1, 8), -5, 5)}
def build(rng, n, lo=-10**9, hi=10**9, shape="random"):
    a = ints(rng, n, lo, hi)
    if shape == "sorted":
        a.sort()
    elif shape == "reversed":
        a.sort(reverse=True)
    return {"scores": a}
