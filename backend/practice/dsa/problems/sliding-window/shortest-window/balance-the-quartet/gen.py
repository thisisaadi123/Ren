def build(rng, n, skew=0):
    n -= n % 4
    if skew:
        weights = [skew, 1, 1, 1]
        return {"s": "".join(rng.choices("SATB", weights, k=n))}
    if rng.random() < 0.2:
        s = list("SATB" * (n // 4))
        rng.shuffle(s)
        return {"s": "".join(s)}
    return {"s": "".join(rng.choice("SATB") for _ in range(n))}


def small(rng):
    return build(rng, rng.choice((4, 8)), rng.choice((0, 0, 3)))
