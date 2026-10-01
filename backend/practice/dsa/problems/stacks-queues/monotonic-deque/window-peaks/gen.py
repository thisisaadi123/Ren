from ren_gen import ints


def build(rng, n, k=0, lo=-10**4, hi=10**4, shape="random"):
    a = ints(rng, n, lo, hi)
    if shape == "descending":
        a.sort(reverse=True)
    elif shape == "ascending":
        a.sort()
    return {"temps": a, "k": min(k or rng.randint(1, n), n)}


def small(rng):
    n = rng.randint(1, 8)
    return build(rng, n, rng.randint(1, n), -3, rng.choice((3, 10)), rng.choice(("random", "random", "descending")))
