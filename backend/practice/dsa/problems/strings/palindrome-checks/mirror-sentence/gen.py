import string
NOISE = " ,.!?'-:;"
def mirror(rng, n, alpha, noise):
    half = [rng.choice(alpha) for _ in range(n // 2)]
    core = half + ([rng.choice(alpha)] if n % 2 else []) + half[::-1]
    out = []
    for c in core:
        if rng.random() < 0.3:
            c = c.swapcase()
        out.append(c)
        if rng.random() < noise:
            out.append(rng.choice(NOISE))
    return "".join(out)
def make(rng, n, alpha, noise, shape):
    s = mirror(rng, n, alpha, noise)
    if shape == "flaw":
        idx = [i for i, c in enumerate(s) if c.isalnum()]
        if idx:
            i = rng.choice(idx)
            s = s[:i] + rng.choice([c for c in alpha if c.lower() != s[i].lower()]) + s[i + 1:]
    elif shape == "random":
        s = "".join(rng.choice(alpha + NOISE) for _ in range(n))
    return s or "a"
def small(rng):
    return {"text": make(rng, rng.randint(1, 12), "abAB1 ", 0.3, rng.choice(["ok", "flaw", "random"]))}
def build(rng, n, alpha="mixed", noise=0.2, shape="ok"):
    alpha = {"mixed": string.ascii_letters + string.digits, "ab": "aAbB", "digits": "0123456789"}[alpha]
    return {"text": make(rng, n, alpha, noise, shape)[:2 * 10**5]}
