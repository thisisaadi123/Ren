def build(rng, n=36, hi=10**7, neg=1, goal=10**8):
    lo = -hi if neg else 1
    return {"nums": [rng.randint(lo, hi) for _ in range(n)], "goal": rng.randint(-goal, goal)}


def small(rng):
    return build(rng, rng.randint(1, 10), 20, rng.choice((0, 1)), 60)
