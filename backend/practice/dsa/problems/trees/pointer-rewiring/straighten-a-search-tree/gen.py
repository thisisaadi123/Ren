import sys
sys.path.insert(0, "")
from ren_gen import bst, distinct


def chain(keys, side):
    out = [keys[0]]
    for k in keys[1:]:
        out += [None, k] if side == "right" else [k, None]
    while out and out[-1] is None:
        out.pop()
    return out


def build(rng, n, order="random"):
    if order == "left":
        return {"root": chain(sorted(distinct(rng, n, 0, 10**5), reverse=True), "left")}
    if order == "right":
        return {"root": chain(sorted(distinct(rng, n, 0, 10**5)), "right")}
    return {"root": bst(rng, n, 0, 10**5, order=order)}


def small(rng):
    return build(rng, rng.randint(1, 8), rng.choice(("random", "random", "balanced", "left")))
