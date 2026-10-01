from ren_gen import ints


def small(rng):
    return {"ratings": ints(rng, rng.randint(1, 6), 0, 3)}


def build(rng, n, hi=100, shape="random"):
    a = ints(rng, n, 0, hi)
    if shape == "ascending":
        a.sort()
    elif shape == "equal":
        a = [rng.randint(0, hi)] * n
    elif shape == "deep":
        a = [hi] + sorted(ints(rng, n - 1, 0, hi - 1))
    elif shape == "tail":
        k = min(n, rng.randint(2, 60))
        a[n - k:] = sorted(a[n - k:])
    return {"ratings": a}
