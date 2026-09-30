def small(rng):
    return {"text": "".join(rng.choice("ab") for _ in range(rng.randint(1, 9)))}
def build(rng, n, alphabet="abc", run=5):
    out = []
    while len(out) < n:
        out += [rng.choice(alphabet)] * rng.randint(1, run)
    return {"text": "".join(out[:n])}
