def reading(rng, n, nines=False):
    d = [9] * n if nines else [rng.randint(0, 9) for _ in range(n)]
    if d[0] == 0 and n > 1:
        d[0] = rng.randint(1, 9)
    return d


def build(rng, n, m=0, shape="random"):
    m = m or n
    if shape == "carry":
        return {"a": reading(rng, n, True), "b": [1]}
    if shape == "nines":
        return {"a": reading(rng, n, True), "b": reading(rng, m, True)}
    return {"a": reading(rng, n), "b": reading(rng, m)}


def small(rng):
    if rng.random() < 0.2:
        return build(rng, rng.randint(1, 5), shape="carry")
    return build(rng, rng.randint(1, 5), rng.randint(1, 5), rng.choice(("random", "random", "nines")))
