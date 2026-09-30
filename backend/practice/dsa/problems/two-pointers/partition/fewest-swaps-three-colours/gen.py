from ren_gen import ints
def small(rng):
    return {"balls": ints(rng, rng.randint(1, 8), 0, 2)}
def build(rng, n, shape="random"):
    if shape == "rotated":
        k = n // 3
        a = [1] * k + [2] * k + [0] * (n - 2 * k)
    elif shape == "near":
        a = sorted(ints(rng, n, 0, 2))
        for _ in range(5):
            i, j = rng.randrange(n), rng.randrange(n)
            a[i], a[j] = a[j], a[i]
    else:
        a = ints(rng, n, 0, 2)
    return {"balls": a}
