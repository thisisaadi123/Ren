def build(rng, n, hi=1000, cap=-1, ones=0):
    a = [1 if rng.random() < ones / 100 else rng.randint(1, hi) for _ in range(n)]
    return {"factors": a, "cap": cap if cap >= 0 else rng.randint(0, 10**6)}


def small(rng):
    return build(rng, rng.randint(1, 8), rng.choice((3, 10)), rng.randint(0, 60), rng.choice((0, 40)))
