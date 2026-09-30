def mirror(rng, n, digits):
    half = [rng.randint(0, digits) for _ in range(n // 2)]
    mid = [rng.randint(0, digits)] if n % 2 else []
    return half + mid + half[::-1]


def small(rng):
    n = rng.randint(1, 9)
    if rng.random() < 0.5:
        return {"head": mirror(rng, n, 2)}
    return {"head": [rng.randint(0, 2) for _ in range(n)]}


def build(rng, n, shape="mirror", digits=9):
    if shape == "mirror":
        return {"head": mirror(rng, n, digits)}
    if shape == "near":  # a mirror with one digit changed near the middle or an end
        h = mirror(rng, n, digits)
        i = rng.choice([0, n - 1, n // 2 - 1, n // 2, rng.randrange(n)])
        h[i] = (h[i] + 1) % 10
        if h == h[::-1]:
            h[0] = (h[-1] + 1) % 10
        return {"head": h}
    if shape == "same":
        return {"head": [4] * n}
    return {"head": [rng.randint(0, digits) for _ in range(n)]}
