def build(rng, n, hi=1000, right=50, shape="random"):
    def one(sign):
        return sign * rng.randint(1, hi)
    if shape == "wall":
        k = n // 2
        return {"comets": [one(1) for _ in range(k)] + [-hi] + [one(-1) for _ in range(n - k - 1)]}
    if shape == "pairs":
        out = []
        while len(out) < n:
            v = rng.randint(1, hi)
            out += [v, -v]
        return {"comets": out[:n] if n > 1 else [1, -1]}
    return {"comets": [one(1 if rng.random() < right / 100 else -1) for _ in range(n)]}


def small(rng):
    return build(rng, rng.randint(2, 8), rng.choice((3, 10)), rng.choice((30, 50, 70)), rng.choice(("random", "random", "pairs")))
