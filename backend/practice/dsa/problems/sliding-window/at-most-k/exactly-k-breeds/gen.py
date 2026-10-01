def build(rng, n, kinds=0, k=0, runs=0):
    kinds = min(kinds or n, n)
    if runs:
        a = []
        while len(a) < n:
            a += [rng.randint(1, kinds)] * rng.randint(1, runs)
        a = a[:n]
    else:
        a = [rng.randint(1, kinds) for _ in range(n)]
    return {"pens": a, "k": min(k or rng.randint(1, kinds), n)}


def small(rng):
    n = rng.randint(1, 8)
    return build(rng, n, rng.randint(1, min(n, 4)), 0, rng.choice((0, 0, 3)))
