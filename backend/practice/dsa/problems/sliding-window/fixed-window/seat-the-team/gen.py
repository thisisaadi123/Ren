def build(rng, n, ones=50, shape="random"):
    if shape == "split":
        k = n * ones // 100
        a = [1] * (k // 2) + [0] * (n - k) + [1] * (k - k // 2)
        return {"seats": a}
    return {"seats": [1 if rng.random() < ones / 100 else 0 for _ in range(n)]}


def small(rng):
    return build(rng, rng.randint(1, 8), rng.choice((20, 50, 80)), rng.choice(("random", "random", "split")))
