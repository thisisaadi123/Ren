from ren_gen import word

LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def build(rng, n, m, alpha=4, shape="random"):
    letters = LETTERS[:alpha]
    s = word(rng, n, letters)
    if shape == "inside":
        # t is a shuffled piece of s, so an answer exists.
        i = rng.randint(0, n - m)
        piece = list(s[i:i + m])
        rng.shuffle(piece)
        t = "".join(piece)
    elif shape == "spread":
        # t's letters sit at the two ends of s.
        s = "x" + "a" * (n - 2) + "y"
        t = "xy" + "a" * (m - 2)
    elif shape == "case":
        t = word(rng, m, letters.upper() + letters)
    else:
        t = word(rng, m, letters)
    return {"s": s, "t": t}


def small(rng):
    n = rng.randint(1, 9)
    return build(rng, n, rng.randint(1, min(n, 4)) if rng.random() < 0.8 else rng.randint(1, 4),
                 rng.choice((2, 3, 4)), rng.choice(("random", "inside", "inside")))
