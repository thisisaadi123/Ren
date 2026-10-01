from ren_gen import ints


def build(rng, n, hi=10**4, target=0):
    a = ints(rng, n, 1, hi)
    if not target:
        target = rng.randint(1, sum(a) + hi)
    return {"gains": a, "target": min(target, 10**9)}


def small(rng):
    return build(rng, rng.randint(1, 8), rng.choice((3, 10)), rng.randint(1, 40))
