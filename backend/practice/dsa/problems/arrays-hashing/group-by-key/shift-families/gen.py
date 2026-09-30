from ren_gen import word
def fam(rng, n, bases, max_len):
    roots = [word(rng, rng.randint(1, max_len)) for _ in range(bases)]
    out = []
    for _ in range(n):
        r, k = rng.choice(roots), rng.randrange(26)
        out.append("".join(chr((ord(c) - 97 + k) % 26 + 97) for c in r))
    return out
def small(rng):
    return {"words": fam(rng, rng.randint(1, 6), rng.randint(1, 4), 3)}
def build(rng, n, bases=0, max_len=8):
    return {"words": fam(rng, n, bases or max(1, n // 3), max_len)}
