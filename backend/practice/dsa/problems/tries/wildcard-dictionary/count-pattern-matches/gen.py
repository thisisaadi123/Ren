def vocab(rng, count, lo, hi, alpha):
    return ["".join(rng.choice(alpha) for _ in range(rng.randint(lo, hi))) for _ in range(count)]


def build(rng, n, q=0, alpha="abc", lo=1, hi=5):
    q = q or n
    words = vocab(rng, n, lo, hi, alpha)
    patterns = []
    for _ in range(q):
        w = list(rng.choice(words))
        for i in rng.sample(range(len(w)), min(len(w), rng.randint(0, 2))):
            w[i] = "."
        if rng.random() < 0.1:
            w = w + [rng.choice(alpha)] if len(w) < 10 else w[:-1]
        patterns.append("".join(w))
    return {"words": words, "patterns": patterns}


def small(rng):
    return build(rng, rng.randint(1, 6), rng.randint(1, 4), "ab", 1, 3)
