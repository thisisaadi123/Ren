def build(rng, n, rare=-1):
    if rare >= 0:
        s = ["a" if rng.random() < 0.5 else "b" for _ in range(n)]
        for _ in range(rare):
            s[rng.randrange(n)] = "c"
        return {"s": "".join(s)}
    return {"s": "".join(rng.choice("abc") for _ in range(n))}


def small(rng):
    return build(rng, rng.randint(3, 9), rng.choice((-1, -1, 1)))
