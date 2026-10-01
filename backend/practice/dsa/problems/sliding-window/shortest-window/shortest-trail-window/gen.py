from ren_gen import word

LOW = "abcdefghijklmnopqrstuvwxyz"


def build(rng, n, m, alpha=3, shape="random"):
    letters = LOW[:alpha]
    if shape == "rare-end":
        return {"s": "a" * (n - 1) + "b", "t": "a" * (m - 1) + "b"}
    if shape == "same":
        return {"s": "a" * n, "t": "a" * m}
    s = word(rng, n, letters)
    if shape == "inside":
        idx = sorted(rng.sample(range(n), m))
        t = "".join(s[i] for i in idx)
    else:
        t = word(rng, m, letters)
    return {"s": s, "t": t}


def small(rng):
    n = rng.randint(1, 9)
    m = rng.randint(1, min(n, 3)) if rng.random() < 0.8 else rng.randint(1, 4)
    return build(rng, n, m, rng.choice((2, 3)), rng.choice(("random", "inside")) if m <= n else "random")
