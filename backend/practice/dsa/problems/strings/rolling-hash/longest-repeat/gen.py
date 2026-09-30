from ren_gen import word
def small(rng):
    return {"s": word(rng, rng.randint(1, 12), "abc"[:rng.randint(1, 3)])}
def build(rng, n, alpha="abcdefghijklmnopqrstuvwxyz", shape="random"):
    if shape == "same":
        return {"s": "a" * n}
    if shape == "planted":
        s = list(word(rng, n, alpha))
        L = n // 4
        piece = word(rng, L, alpha)
        i, j = rng.randrange(0, n // 2 - L), rng.randrange(n // 2, n - L)
        s[i:i + L] = piece
        s[j:j + L] = piece
        return {"s": "".join(s)}
    if shape == "distinct":
        return {"s": "abcdefghijklmnopqrstuvwxyz"[:min(n, 26)]}
    return {"s": word(rng, n, alpha)}
