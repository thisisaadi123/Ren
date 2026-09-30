from ren_gen import ints
def small(rng):
    return {"nums": ints(rng, rng.randint(1, 8), -3, 6), "k": rng.randint(0, 4)}
def build(rng, n, spread=10**7, k=-1):
    return {"nums": ints(rng, n, -spread, spread), "k": k if k >= 0 else rng.randint(0, min(spread, 10**7))}
