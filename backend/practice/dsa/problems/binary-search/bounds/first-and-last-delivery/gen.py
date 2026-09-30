from ren_gen import ints
def make(rng, n, spread, hit):
    a = sorted(ints(rng, n, -spread, spread))
    t = rng.choice(a) if hit and a else rng.randint(-spread, spread)
    return {"times": a, "target": t}
def small(rng):
    return make(rng, rng.randint(0, 8), 4, rng.random() < 0.6)
def build(rng, n, spread=1000, hit=1):
    return make(rng, n, spread, bool(hit))
