from ren_gen import ints


def build(rng, n, hi=10**9, limit=-1, shape="random"):
    if shape == "walk":
        a, v = [], hi // 2
        for _ in range(n):
            v = min(hi, max(1, v + rng.randint(-3, 3)))
            a.append(v)
    else:
        a = ints(rng, n, 1, hi)
    if shape == "ascending":
        a.sort()
    return {"readings": a, "limit": limit if limit >= 0 else rng.randint(0, hi)}


def small(rng):
    hi = rng.choice((5, 20))
    return build(rng, rng.randint(1, 8), hi, rng.randint(0, hi))
