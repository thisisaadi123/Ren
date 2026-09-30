def make(rng, n, shape):
    if shape == "perm":
        a = list(range(1, n + 1))
    elif shape == "gap":
        gap = rng.randint(1, n)
        a = [x for x in range(1, n + 2) if x != gap][:n]
    elif shape == "junk":
        a = [rng.choice([rng.randint(-2**31, 0), rng.randint(n + 1, 2**31 - 1)]) for _ in range(n)]
    elif shape == "dups":
        a = [rng.randint(1, max(1, n // 3)) for _ in range(n)]
    else:
        a = [rng.randint(-n, 2 * n) for _ in range(n)]
    rng.shuffle(a)
    return {"nums": a}
def small(rng):
    return make(rng, rng.randint(1, 8), rng.choice(["perm", "gap", "junk", "dups", "mix"]))
def build(rng, n, shape="mix"):
    return make(rng, n, shape)
