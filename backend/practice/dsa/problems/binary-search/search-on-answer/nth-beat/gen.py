def small(rng):
    return {"n": rng.randint(1, 40), "a": rng.randint(2, 9), "b": rng.randint(2, 9)}
def build(rng, n, hi=40_000, shape="random"):
    a = rng.randint(2, hi)
    b = {"same": a, "multiple": min(hi, a * rng.randint(1, 3)), "coprime": a + 1 if a < hi else a - 1}.get(shape, rng.randint(2, hi))
    return {"n": rng.randint(max(1, n // 2), n), "a": a, "b": b}
