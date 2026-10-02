def build(rng, n, alpha="ab"):
    return {"s": "".join(rng.choice(alpha) for _ in range(n))}


def small(rng):
    return build(rng, rng.randint(1, 6), rng.choice(("ab", "abc", "a")))
