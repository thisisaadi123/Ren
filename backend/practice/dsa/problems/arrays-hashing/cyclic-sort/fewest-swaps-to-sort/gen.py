def small(rng):
    return build(rng, rng.randint(1, 8))
def build(rng, n, shape="random"):
    a = list(range(1, n + 1))
    if shape == "random":
        rng.shuffle(a)
    elif shape == "reversed":
        a.reverse()
    elif shape == "shift":
        a = a[1:] + a[:1]
    elif shape == "near":
        for _ in range(3):
            i, j = rng.randrange(n), rng.randrange(n)
            a[i], a[j] = a[j], a[i]
    return {"order": a}
