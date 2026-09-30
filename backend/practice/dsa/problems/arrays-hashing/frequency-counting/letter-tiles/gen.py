from ren_gen import word


def small(rng):
    a = "abc"[: rng.randint(1, 3)]
    return {"sign": word(rng, rng.randint(1, 6), a), "tiles": word(rng, rng.randint(1, 8), a)}


def build(rng, n, shape="random"):
    tiles = word(rng, n)
    if shape == "exact":  # the sign uses every tile exactly once
        s = list(tiles)
        rng.shuffle(s)
        return {"sign": "".join(s), "tiles": tiles}
    if shape == "one-short":  # needs one more copy of a letter than there are tiles
        tiles = tiles[: n - 1]
        s = list(tiles) + [tiles[0]]
        rng.shuffle(s)
        return {"sign": "".join(s), "tiles": tiles}
    return {"sign": word(rng, max(1, n // 2)), "tiles": tiles}
