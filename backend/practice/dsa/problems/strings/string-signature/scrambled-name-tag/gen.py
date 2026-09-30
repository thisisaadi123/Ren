import string
def scramble(rng, a, spaces):
    letters = [c.swapcase() if rng.random() < 0.3 else c for c in a if c != " "]
    rng.shuffle(letters)
    out = []
    for c in letters:
        out.append(c)
        if rng.random() < spaces:
            out.append(" ")
    return "".join(out).strip() or letters[0]
def phrase(rng, n, alpha, spaces):
    s = "".join(" " if rng.random() < spaces else rng.choice(alpha) for _ in range(n))
    return s if s.strip() else rng.choice(alpha) + s[1:]
def make(rng, n, alpha, spaces, shape):
    a = phrase(rng, n, alpha, spaces)
    if shape == "random":
        return {"a": a, "b": phrase(rng, n, alpha, spaces)}
    b = scramble(rng, a, spaces)
    if shape == "near":
        i = rng.choice([k for k, c in enumerate(b) if c != " "])
        b = b[:i] + rng.choice([x for x in alpha if x.lower() != b[i].lower()]) + b[i + 1:]
    return {"a": a, "b": b}
def small(rng):
    return make(rng, rng.randint(1, 10), "abAB", 0.2, rng.choice(["random", "same", "near"]))
def build(rng, n, alpha="low", spaces=0.15, shape="same"):
    alpha = {"low": "abcdefghijklmnopqrstuvwxyz", "mixed": string.ascii_letters, "ab": "abAB"}[alpha]
    return make(rng, n, alpha, spaces, shape)
