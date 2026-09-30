from ren_gen import ints
def small(rng):
    return {"ropes": ints(rng, rng.randint(1, 4), 1, 20), "pieces": rng.randint(1, 8)}
def build(rng, n, hi=10**7, pieces=0):
    return {"ropes": ints(rng, n, 1, hi), "pieces": pieces or rng.randint(1, 10**6)}
