def small(rng):
    text = "".join(rng.choice("abc") for _ in range(rng.randint(1, 8)))
    return {"text": text, "words": ["".join(rng.choice("abc") for _ in range(rng.randint(1, 3))) for _ in range(rng.randint(1, 5))]}
def build(rng, n, count=500, maxlen=50, alphabet="abcdefghijklmnopqrstuvwxyz"):
    text = "".join(rng.choice(alphabet) for _ in range(n))
    words = []
    for _ in range(count):
        k = rng.randint(1, maxlen)
        if rng.random() < 0.5:
            idx = sorted(rng.sample(range(n), min(k, n)))
            words.append("".join(text[i] for i in idx))
        else:
            words.append("".join(rng.choice(alphabet) for _ in range(k)))
    return {"text": text, "words": words}
