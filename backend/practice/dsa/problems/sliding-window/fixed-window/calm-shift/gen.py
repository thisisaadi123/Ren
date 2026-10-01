from ren_gen import ints


def build(rng, n, minutes=0, mood=50, hi=1000):
    return {
        "customers": ints(rng, n, 0, hi),
        "moody": [1 if rng.random() < mood / 100 else 0 for _ in range(n)],
        "minutes": min(minutes or rng.randint(1, n), n),
    }


def small(rng):
    n = rng.randint(1, 8)
    return build(rng, n, rng.randint(1, n), rng.choice((30, 50, 80)), rng.choice((5, 1000)))
