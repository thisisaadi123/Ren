from ren_gen import ints
def small(rng):
    l = ints(rng, rng.randint(1, 6), 1, 20)
    return {"loads": l, "threshold": rng.randint(len(l), len(l) + 30)}
def build(rng, n, hi=10**6, slack=-1):
    l = ints(rng, n, 1, hi)
    t = n + (slack if slack >= 0 else rng.randint(0, 10 * n))
    return {"loads": l, "threshold": min(10**6, t)}
