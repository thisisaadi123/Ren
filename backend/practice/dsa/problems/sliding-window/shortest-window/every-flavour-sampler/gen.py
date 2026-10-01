def build(rng, n, kinds=5, shape="random"):
    labels = [rng.randint(1, 10**9) for _ in range(kinds)]
    if shape == "ends":
        a = [labels[0]] + [rng.choice(labels[1:] or labels) for _ in range(n - 2)] + [labels[0]]
        a = a[:n]
        if n > 2:
            a[n // 2] = labels[-1]
        return {"jars": a}
    if shape == "rare":
        a = [rng.choice(labels[:-1] or labels) for _ in range(n)]
        a[rng.randrange(n)] = labels[-1]
        return {"jars": a}
    return {"jars": [rng.choice(labels) for _ in range(n)]}


def small(rng):
    return build(rng, rng.randint(1, 9), rng.randint(1, 4), rng.choice(("random", "random", "rare")))
