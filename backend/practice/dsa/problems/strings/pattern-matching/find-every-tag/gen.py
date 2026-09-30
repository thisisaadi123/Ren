from ren_gen import word
def small(rng):
    al = "ab"[:rng.randint(1, 2)]
    t = word(rng, rng.randint(1, 12), al)
    return {"text": t, "tag": word(rng, rng.randint(1, min(3, len(t))), al)}
def build(rng, n, m, alpha="ab", shape="random"):
    if shape == "same":
        return {"text": "a" * n, "tag": "a" * m}
    if shape == "near":
        return {"text": "a" * n, "tag": "a" * (m - 1) + "b"}
    return {"text": word(rng, n, alpha), "tag": word(rng, m, alpha)}
