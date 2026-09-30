def small(rng):
    return {"word": "".join(rng.choice("abc") for _ in range(rng.randint(0, 3))), "text": "".join(rng.choice("abc") for _ in range(rng.randint(0, 7)))}
def build(rng, n, w=50, alphabet="abcdefghijklmnopqrstuvwxyz", hidden=True):
    text = "".join(rng.choice(alphabet) for _ in range(n))
    if hidden not in (False, "false") and n >= w:
        idx = sorted(rng.sample(range(n), w))
        word = "".join(text[i] for i in idx)
    else:
        word = "".join(rng.choice(alphabet) for _ in range(w))
    return {"word": word, "text": text}
