from ren_gen import word
def make(rng, count, bases, max_len):
    roots = [word(rng, rng.randint(0, max_len), "abcdef") for _ in range(bases)]
    out = []
    for _ in range(count):
        letters = list(rng.choice(roots))
        rng.shuffle(letters)
        out.append("".join(letters))
    return out
def small(rng):
    return {"words": make(rng, rng.randint(1, 6), rng.randint(1, 3), 3)}
def build(rng, n, bases=0, max_len=8):
    return {"words": make(rng, n, bases or max(1, n // 4), max_len)}
