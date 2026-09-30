from ren_gen import ints
def small(rng):
    return {"values": ints(rng, rng.randint(3, 7), -9, 9), "target": rng.randint(-30, 30)}
def build(rng, n, hi=1000, t=10**4):
    return {"values": ints(rng, n, -hi, hi), "target": rng.randint(-t, t)}
