def build(rng, n, kinds=0, runs=0):
    kinds = min(kinds or n, n)
    if runs:
        out = []
        while len(out) < n:
            out += [rng.randrange(kinds)] * rng.randint(1, runs)
        return {"flavours": out[:n]}
    return {"flavours": [rng.randrange(kinds) for _ in range(n)]}


def small(rng):
    n = rng.randint(1, 9)
    return build(rng, n, rng.randint(1, 4), rng.choice((0, 3)))
