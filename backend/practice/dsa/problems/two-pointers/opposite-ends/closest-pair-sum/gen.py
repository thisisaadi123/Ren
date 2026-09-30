from ren_gen import ints
def small(rng):
    return {"nums": ints(rng, rng.randint(2, 8), -9, 9), "target": rng.randint(-20, 20)}
def build(rng, n, hi=10**9):
    return {"nums": ints(rng, n, -hi, hi), "target": rng.randint(-2 * hi, 2 * hi)}
