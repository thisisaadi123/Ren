def mountain(rng, n, top=None):
    t = rng.randint(1, n - 2) if top is None else top
    up = sorted(rng.sample(range(0, 10**9 - n), t))
    peak = max(up[-1] + rng.randint(1, n), n)
    down = sorted(rng.sample(range(0, peak), n - t - 1), reverse=True)
    return up + [peak] + down
def small(rng):
    return {"elevations": mountain(rng, rng.randint(3, 8))}
def build(rng, n, where="random"):
    return {"elevations": mountain(rng, n, {"left": 1, "right": n - 2}.get(where))}
