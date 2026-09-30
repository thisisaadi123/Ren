from ren_gen import ints
def small(rng):
    return {"balls": ints(rng, rng.randint(1, 9), 0, 2)}
def build(rng, n, hi=2):
    return {"balls": ints(rng, n, 0, hi)}
