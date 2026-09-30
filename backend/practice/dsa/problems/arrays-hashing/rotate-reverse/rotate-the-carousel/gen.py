from ren_gen import ints
def small(rng):
    return {"slots": ints(rng, rng.randint(1, 7), -9, 9), "k": rng.randint(0, 20)}
def build(rng, n, k=None):
    return {"slots": ints(rng, n, -10**9, 10**9), "k": k if k is not None else rng.randint(0, 10**9)}
