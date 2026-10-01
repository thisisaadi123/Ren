def build(rng, n, k=-1, ones=60):
    return {"status": [1 if rng.random() < ones / 100 else 0 for _ in range(n)],
            "k": k if k >= 0 else rng.randint(0, n)}


def small(rng):
    n = rng.randint(1, 9)
    return build(rng, n, rng.randint(0, min(n, 3)), rng.choice((30, 60, 90)))
