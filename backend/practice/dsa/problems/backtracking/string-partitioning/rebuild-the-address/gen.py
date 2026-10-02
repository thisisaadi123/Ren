def build(rng, n, zeros=0):
    if zeros:
        return {"digits": "".join(rng.choice("0012") for _ in range(n))}
    return {"digits": "".join(rng.choice("0123456789") for _ in range(n))}


def small(rng):
    return build(rng, rng.randint(1, 13), rng.choice((0, 1)))
