def vocab(rng, count, lo, hi, alpha):
    return ["".join(rng.choice(alpha) for _ in range(rng.randint(lo, hi))) for _ in range(count)]


def build(rng, n, m=6, alpha="abc", lo=1, hi=8):
    products = vocab(rng, n, lo, hi, alpha)
    base = rng.choice(products)
    typed = (base + "".join(rng.choice(alpha) for _ in range(m)))[:max(1, m)]
    return {"products": products, "typed": typed}


def small(rng):
    return build(rng, rng.randint(1, 6), rng.randint(1, 4), "ab", 1, 4)
