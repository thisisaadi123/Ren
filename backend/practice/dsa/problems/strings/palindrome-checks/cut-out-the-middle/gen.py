import string
def rnd(rng, n, alpha):
    return "".join(rng.choice(alpha) for _ in range(n))
def pal(rng, n, alpha):
    h = rnd(rng, n // 2, alpha)
    return h + (rng.choice(alpha) if n % 2 else "") + h[::-1]
def make(rng, n, alpha, shape, outer):
    x = rnd(rng, outer, alpha)
    m = n - 2 * outer
    if shape == "random":
        mid = rnd(rng, m, alpha)
    elif shape == "pal":
        mid = pal(rng, m, alpha)
    elif shape == "palmid":
        k = rng.randint(m // 3, max(m // 3, m - 1))
        p = pal(rng, k, alpha)
        rest = rnd(rng, m - k, alpha)
        mid = p + rest if rng.random() < 0.5 else rest + p
    elif shape == "slow":
        k = m // 2
        mid = "a" * k + "c" + "a" * (m - k - 2) + "d"
        if rng.random() < 0.5:
            mid = mid[::-1]
    else:
        raise ValueError(shape)
    return x + mid + x[::-1]
def small(rng):
    n = rng.randint(1, 12)
    return {"s": make(rng, n, "abc"[:rng.randint(1, 3)], rng.choice(["random", "random", "pal", "palmid"]), rng.randint(0, n // 2))}
def build(rng, n, k=26, shape="random", outer=0):
    return {"s": make(rng, n, string.ascii_lowercase[:k], shape, outer)}
