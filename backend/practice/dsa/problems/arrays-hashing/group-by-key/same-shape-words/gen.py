from ren_gen import word
def small(rng):
    a = rng.choice(["ab", "abc"])
    return {"words": [word(rng, rng.randint(1, 4), a) for _ in range(rng.randint(1, 5))], "pattern": word(rng, rng.randint(1, 4), a)}
def build(rng, n, length=4, alphabet="abcd"):
    return {"words": [word(rng, length, alphabet) for _ in range(n)], "pattern": word(rng, length, alphabet)}
