from ren_gen import ints
def small(rng):
    return {"nums": ints(rng, rng.randint(1, 8), 0, 12), "k": rng.randint(1, 6)}
def build(rng, n, k=0, hi=10**9):
    return {"nums": ints(rng, n, 0, hi), "k": k or rng.randint(1, 100_000)}
