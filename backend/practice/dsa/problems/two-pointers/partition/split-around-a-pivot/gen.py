from ren_gen import ints
def small(rng):
    return {"values": ints(rng, rng.randint(1, 8), -3, 3), "pivot": rng.randint(-3, 3)}
def build(rng, n, hi=10**6):
    v = ints(rng, n, -hi, hi)
    return {"values": v, "pivot": rng.choice(v)}
