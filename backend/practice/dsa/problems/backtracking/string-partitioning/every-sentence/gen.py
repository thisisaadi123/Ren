def build(rng, n, k=6, alpha="ab"):
    vocab = sorted({"".join(rng.choice(alpha) for _ in range(rng.randint(1, 3))) for _ in range(k * 3)})[:k]
    text = ""
    while len(text) < n:
        text += rng.choice(vocab)
    return {"text": text[:n], "words": vocab}


def small(rng):
    return build(rng, rng.randint(1, 8), rng.randint(1, 4), "ab")
