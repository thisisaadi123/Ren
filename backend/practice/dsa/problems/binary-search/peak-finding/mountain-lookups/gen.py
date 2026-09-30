def mountain(rng, n, spread):
    t = rng.randint(1, n - 2)
    up = sorted(rng.sample(range(0, spread), t))
    peak = max(up[-1] + rng.randint(1, 5), n + 1)
    down = sorted(rng.sample(range(0, peak), n - t - 1), reverse=True)
    return up + [peak] + down
def make(rng, n, m, spread):
    e = mountain(rng, n, spread)
    ts = [rng.choice(e) if rng.random() < 0.7 else rng.randint(0, spread + 5) for _ in range(m)]
    return {"elevations": e, "targets": ts}
def small(rng):
    return make(rng, rng.randint(3, 8), rng.randint(1, 5), 12)
def build(rng, n, m, spread=10**9 - 10):
    return make(rng, n, m, max(spread, n + 5))
