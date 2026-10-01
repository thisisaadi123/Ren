from ren_gen import word


def build(rng, n, k=0, alpha="mixed"):
    letters = {"mixed": "aeioubcdy", "full": "abcdefghijklmnopqrstuvwxyz", "consonants": "bcdfghy"}[alpha]
    return {"s": word(rng, n, letters), "k": min(k or rng.randint(1, n), n)}


def small(rng):
    n = rng.randint(1, 8)
    return build(rng, n, rng.randint(1, n), rng.choice(("mixed", "full")))
