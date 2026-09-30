from ren_gen import distinct
def small(rng):
    return {"stations": sorted(distinct(rng, rng.randint(2, 6), 0, 60)), "extra": rng.randint(1, 12)}
def build(rng, n, extra=0, hi=10**8):
    return {"stations": sorted(distinct(rng, n, 0, hi)), "extra": extra or rng.randint(1, 10**6)}
