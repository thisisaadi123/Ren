from ren_gen import word


def nested(rng, depth, k, alpha):
    """A string that collapses completely: runs of k wrapped around each other."""
    if depth == 0:
        return ""
    c = rng.choice(alpha)
    inner = nested(rng, depth - 1, k, [x for x in alpha if x != c] or alpha)
    cut = rng.randint(1, k - 1)
    return c * cut + inner + c * (k - cut)


def build(rng, n, k=2, alpha=3, shape="random"):
    letters = "abcdefghijklmnopqrstuvwxyz"[:alpha]
    if shape == "nested":
        out = ""
        while len(out) < n:
            out += nested(rng, min(30, max(1, (n - len(out)) // k)), k, list(letters))
        return {"s": out[:n], "k": k}
    if shape == "runs":
        out = []
        while len(out) < n:
            out += [rng.choice(letters)] * rng.randint(1, k + 1)
        return {"s": "".join(out[:n]), "k": k}
    return {"s": word(rng, n, letters), "k": k}


def small(rng):
    return build(rng, rng.randint(1, 10), rng.choice((2, 3)), rng.choice((2, 3)), rng.choice(("random", "nested", "runs")))
