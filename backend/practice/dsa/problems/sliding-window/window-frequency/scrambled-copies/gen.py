from ren_gen import word as letters

LOW = "abcdefghijklmnopqrstuvwxyz"


def build(rng, n, m, alpha=3, shape="random"):
    abc = LOW[:alpha]
    if shape == "same":
        return {"text": "a" * n, "word": "a" * m}
    w = letters(rng, m, abc)
    if shape == "planted":
        parts, size = [], 0
        while size < n:
            if rng.random() < 0.5:
                piece = list(w)
                rng.shuffle(piece)
                piece = "".join(piece)
            else:
                piece = letters(rng, rng.randint(1, m), abc)
            parts.append(piece)
            size += len(piece)
        return {"text": "".join(parts)[:n], "word": w}
    return {"text": letters(rng, n, abc), "word": w}


def small(rng):
    n = rng.randint(1, 9)
    return build(rng, n, rng.randint(1, 4), rng.choice((2, 3)), rng.choice(("random", "planted")))
