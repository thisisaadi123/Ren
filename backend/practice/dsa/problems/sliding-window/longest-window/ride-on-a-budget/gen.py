from ren_gen import ints


def build(rng, n, hi=10**4, budget=-1):
    a = ints(rng, n, 1, hi)
    if budget < 0:
        budget = rng.randint(0, sum(a))
    return {"fares": a, "budget": min(budget, 10**9)}


def small(rng):
    return build(rng, rng.randint(1, 8), rng.choice((3, 10)), rng.randint(0, 30))
