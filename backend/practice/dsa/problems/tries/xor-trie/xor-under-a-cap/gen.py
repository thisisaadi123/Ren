def build(rng, n, q=0, hi=10**9, low_caps=0):
    q = q or n
    nums = [rng.randint(0, hi) for _ in range(n)]
    queries = []
    for _ in range(q):
        m = rng.randint(0, hi // 50) if rng.randrange(100) < low_caps else rng.randint(0, hi)
        queries.append([rng.randint(0, hi), m])
    return {"nums": nums, "queries": queries}


def small(rng):
    return build(rng, rng.randint(1, 6), rng.randint(1, 5), rng.choice((7, 30)), rng.choice((0, 50)))
