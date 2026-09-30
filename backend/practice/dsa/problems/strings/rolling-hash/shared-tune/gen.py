from ren_gen import word
def small(rng):
    al = "abc"[:rng.randint(1, 3)]
    return {"a": word(rng, rng.randint(1, 8), al), "b": word(rng, rng.randint(1, 8), al)}
def build(rng, n, m=None, alpha="abcdefghijklmnopqrstuvwxyz", share=0, shape="random"):
    m = m or n
    if shape == "same":
        return {"a": "a" * n, "b": "a" * m}
    if shape == "disjoint":
        return {"a": word(rng, n, "abcdefghijklm"), "b": word(rng, m, "nopqrstuvwxyz")}
    a, b = list(word(rng, n, alpha)), list(word(rng, m, alpha))
    if share:
        piece = word(rng, share, alpha)
        i, j = rng.randrange(n - share + 1), rng.randrange(m - share + 1)
        a[i:i + share] = piece
        b[j:j + share] = piece
    return {"a": "".join(a), "b": "".join(b)}
