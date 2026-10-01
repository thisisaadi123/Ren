from ren_gen import word

LOW = "abcdefghijklmnopqrstuvwxyz"


def build(rng, n, w, L, alpha=2, shape="planted", pool=0):
    abc = LOW[:alpha]
    pool = pool or w
    vocab = [word(rng, L, abc) for _ in range(pool)]
    words = [rng.choice(vocab) for _ in range(w)]
    if shape == "same":
        return {"s": "a" * n, "words": ["a" * L] * w}
    if shape == "planted":
        parts, size = [], 0
        while size < n:
            r = rng.random()
            if r < 0.4:
                chain = words[:]
                rng.shuffle(chain)
                parts.append("".join(chain))
            elif r < 0.8:
                parts.append(rng.choice(vocab))
            else:
                parts.append(word(rng, rng.randint(1, L), abc))
            size += len(parts[-1])
        return {"s": "".join(parts)[:n], "words": words}
    return {"s": word(rng, n, abc), "words": words}


def small(rng):
    n = rng.randint(1, 12)
    return build(rng, n, rng.randint(1, 3), rng.randint(1, 2), 2, rng.choice(("planted", "random")))
