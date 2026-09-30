from ren_gen import ints
def small(rng):
    b = ints(rng, rng.randint(1, 5), 1, 30)
    return {"books": b, "hours": rng.randint(len(b), len(b) + 20)}
def build(rng, n, hi=10**9, slack=0):
    b = ints(rng, n, 1, hi)
    return {"books": b, "hours": n + (slack if slack else rng.randint(0, 5 * n))}
