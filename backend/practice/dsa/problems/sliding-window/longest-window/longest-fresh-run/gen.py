from ren_gen import word

ALL = "abcdefghijklmnopqrstuvwxyz0123456789"


def build(rng, n, alpha=36, shape="random"):
    letters = ALL[:alpha]
    if shape == "cycle":
        return {"s": "".join(letters[i % alpha] for i in range(n))}
    if shape == "palin":
        half = word(rng, n // 2, letters)
        return {"s": (half + half[::-1] + "a")[:n]}
    return {"s": word(rng, n, letters)}


def small(rng):
    return build(rng, rng.randint(1, 9), rng.choice((2, 3, 5, 36)), rng.choice(("random", "random", "palin")))
