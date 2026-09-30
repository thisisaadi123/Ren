from ren_gen import ints
def make(rng, n, spread, runs):
    out = []
    while len(out) < n:
        start = rng.randint(-spread, spread)
        length = rng.randint(1, runs)
        out += list(range(start, min(start + length, 10**9 + 1)))
    out = out[:n]
    rng.shuffle(out)
    return out
def small(rng):
    return {"days": ints(rng, rng.randint(0, 8), -3, 6)}
def build(rng, n, spread=10**9, runs=20):
    return {"days": make(rng, n, spread, runs)}
