import string
L = string.ascii_lowercase
def word(rng, n, alpha):
    return "".join(rng.choice(alpha) for _ in range(n))
def make(rng, n, alpha, shape):
    a = word(rng, n, alpha)
    if shape == "random":
        return {"a": a, "b": word(rng, n + rng.choice([0, 0, 0, 1]), alpha)}
    present = sorted(set(a))
    perm = present[:]
    rng.shuffle(perm)
    relabel = dict(zip(present, perm))
    b = [relabel[c] for c in a]
    rng.shuffle(b)
    missing = [c for c in L if c not in present]
    if shape == "new-letter" and missing:
        x = rng.choice(present)
        y = rng.choice(missing[:len(alpha) + 1])
        b = [y if c == relabel[x] else c for c in b]
    elif shape == "move-one" and len(present) > 1:
        i = rng.randrange(len(b))
        choices = [c for c in present if c != b[i]]
        b[i] = rng.choice(choices)
    return {"a": a, "b": "".join(b)}
def small(rng):
    alpha = L[:rng.randint(1, 4)]
    return make(rng, rng.randint(1, 10), alpha, rng.choice(["random", "close", "close", "new-letter", "move-one"]))
def build(rng, n, k=26, shape="close"):
    return make(rng, n, L[:k], shape)
