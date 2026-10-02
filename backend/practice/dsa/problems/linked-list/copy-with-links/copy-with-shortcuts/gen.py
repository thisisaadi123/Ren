def build(rng, n, shape="random", none=20):
    out = []
    for i in range(n):
        if rng.randrange(100) < none:
            r = None
        elif shape == "self":
            r = i
        elif shape == "back":
            r = rng.randrange(i + 1)
        elif shape == "last":
            r = n - 1
        else:
            r = rng.randrange(n)
        out.append([rng.randint(-10**4, 10**4), r])
    return {"head": out}


def small(rng):
    return build(rng, rng.randint(0, 6), rng.choice(("random", "self", "back")), rng.choice((0, 30)))
