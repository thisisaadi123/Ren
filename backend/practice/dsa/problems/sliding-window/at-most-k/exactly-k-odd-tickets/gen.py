def build(rng, n, k=0, odd=50):
    a = [rng.randint(0, 49999) * 2 + (1 if rng.random() < odd / 100 else 2) for _ in range(n)]
    return {"tickets": a, "k": min(k or rng.randint(1, max(1, n // 4)), n)}


def small(rng):
    n = rng.randint(1, 8)
    return build(rng, n, rng.randint(1, min(n, 3)), rng.choice((30, 50, 80)))
