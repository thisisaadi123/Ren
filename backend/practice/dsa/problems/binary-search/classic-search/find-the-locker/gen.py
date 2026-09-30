from ren_gen import distinct
def make(rng, n, lo, hi, hit):
    a = sorted(distinct(rng, n, lo, hi))
    t = rng.choice(a) if hit else rng.randint(lo, hi)
    return {"lockers": a, "target": t}
def small(rng):
    return make(rng, rng.randint(1, 8), -10, 10, rng.random() < 0.5)
def build(rng, n, hit=1):
    return make(rng, n, -10**9, 10**9, bool(hit))
