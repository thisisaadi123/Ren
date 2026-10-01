from ren_gen import bst, distinct


def chain(keys, side):
    """A one-sided chain in level order: [k0, null, k1, null, ...] for right, [k0, k1, null, k2, ...] for left."""
    out = [keys[0]]
    for k in keys[1:]:
        out += [None, k] if side == "right" else [k, None]
    while out and out[-1] is None:
        out.pop()
    return out


def build(rng, n, shape="random"):
    if shape == "right":
        return {"root": chain(sorted(distinct(rng, n, -10**5, 10**5)), "right")}
    if shape == "left":
        return {"root": chain(sorted(distinct(rng, n, -10**5, 10**5), reverse=True), "left")}
    return {"root": bst(rng, n, -10**5, 10**5, order=shape)}


def small(rng):
    return build(rng, rng.randint(1, 8), rng.choice(("random", "random", "right", "left", "balanced")))
