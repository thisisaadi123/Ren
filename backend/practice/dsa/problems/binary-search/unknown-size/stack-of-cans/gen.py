def small(rng):
    return {"cans": rng.randint(1, 100)}
def build(rng, hi=9 * 10**15, shape="random"):
    if shape == "exact":
        r = rng.randint(1, 134_000_000)
        return {"cans": min(hi, r * (r + 1) // 2)}
    return {"cans": rng.randint(1, hi)}
