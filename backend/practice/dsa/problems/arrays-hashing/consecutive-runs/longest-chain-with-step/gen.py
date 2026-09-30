from ren_gen import ints
def small(rng):
    return {"values": ints(rng, rng.randint(1, 8), -6, 6), "step": rng.randint(1, 3)}
def build(rng, n, step=3, chain=None, lo=-10**6, hi=10**6):
    values = ints(rng, n, lo, hi)
    if chain:
        start = rng.randint(-10**6, 10**6)
        k = min(chain, n)
        values[:k] = [start + i * step for i in range(k)]
    rng.shuffle(values)
    return {"values": values, "step": step}
