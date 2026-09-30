from ren_gen import ints
def small(rng):
    return {"mains": sorted(ints(rng, rng.randint(1, 5), 1, 9)), "sides": sorted(ints(rng, rng.randint(1, 5), 1, 9)), "budget": rng.randint(1, 20)}
def build(rng, n, m, hi=10**9, budget=None):
    return {"mains": sorted(ints(rng, n, 1, hi)), "sides": sorted(ints(rng, m, 1, hi)), "budget": budget or rng.randint(1, 2 * hi)}
