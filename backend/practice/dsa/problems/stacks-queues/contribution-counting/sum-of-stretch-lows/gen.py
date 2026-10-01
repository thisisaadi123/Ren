from ren_gen import ints


def build(rng, n, hi=30000, shape="random"):
    a = ints(rng, n, 1, hi)
    if shape == "ascending":
        a.sort()
    elif shape == "descending":
        a.sort(reverse=True)
    elif shape == "equal":
        a = [rng.randint(1, hi)] * n
    return {"prices": a}


def small(rng):
    return build(rng, rng.randint(1, 8), rng.choice((3, 10)), rng.choice(("random", "random", "equal")))
