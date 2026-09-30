def small(rng):
    m = rng.randint(1, 10)
    k = rng.randint(1, m)
    lo, hi = k * (k + 1) // 2, k * (2 * m - k + 1) // 2
    return {"m": m, "k": k, "target": rng.randint(max(1, lo - 2), min(210, hi + 2))}
def build(rng, m, k=0, shape="random"):
    if not k:
        k = rng.randint(1, m)
    lo, hi = k * (k + 1) // 2, k * (2 * m - k + 1) // 2
    if shape == "middle":
        t = (lo + hi) // 2
    elif shape == "low":
        t = lo
    elif shape == "high":
        t = hi
    else:
        t = rng.randint(lo, hi)
    return {"m": m, "k": k, "target": max(1, min(210, t))}
