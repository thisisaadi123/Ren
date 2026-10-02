def build(rng, n, hi=20000, low=0, high=0):
    nums = [rng.randint(1, hi) for _ in range(n)]
    a = low or rng.randint(1, 20000)
    b = high or rng.randint(a, 20000)
    a, b = min(a, b), max(a, b)
    return {"nums": nums, "low": a, "high": b}


def small(rng):
    hi = rng.choice((8, 30))
    a = rng.randint(1, hi)
    return build(rng, rng.randint(1, 8), hi, a, rng.randint(a, hi + 2))
