from ren_gen import ints
def small(rng):
    b = ints(rng, rng.randint(1, 8), -5, 5)
    return {"bids": b, "k": rng.randint(1, len(b))}
def build(rng, n, lo=-10**4, hi=10**4, k=None):
    return {"bids": ints(rng, n, lo, hi), "k": k or rng.randint(1, n)}
