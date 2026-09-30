def small(rng):
    text = "".join(rng.choice("abc") for _ in range(rng.randint(1, 7)))
    words = ["".join(rng.choice("abc") for _ in range(rng.randint(1, 4))) for _ in range(rng.randint(1, 5))]
    return {"text": text, "dictionary": words}
def build(rng, n, count=200, maxlen=20, alphabet="abcde"):
    text = "".join(rng.choice(alphabet) for _ in range(n))
    words = []
    for _ in range(count):
        k = rng.randint(1, maxlen)
        if rng.random() < 0.5 and n >= k:
            idx = sorted(rng.sample(range(n), k))
            words.append("".join(text[i] for i in idx))
        else:
            words.append("".join(rng.choice(alphabet) for _ in range(k)))
    return {"text": text, "dictionary": words}
