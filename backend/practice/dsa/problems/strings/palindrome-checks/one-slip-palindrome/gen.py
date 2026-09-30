import string
def pal(rng, n, alpha):
    half = [rng.choice(alpha) for _ in range(n // 2)]
    return half + ([rng.choice(alpha)] if n % 2 else []) + half[::-1]
def make(rng, n, alpha, shape):
    if shape == "random":
        return "".join(rng.choice(alpha) for _ in range(n))
    if shape == "flaws":
        s = ["a"] * n
        s[n // 4] = "b"
        s[3 * n // 4 + 1] = "c"
        return "".join(s)
    if shape == "late":
        # the extra letter sits next to the middle, so the first mismatch is deep inside
        s = pal(rng, n - 1, alpha)
        k = (n - 1) // 2 + rng.choice([-1, 0, 1])
        s.insert(max(0, k), rng.choice(alpha))
        return "".join(s)
    s = pal(rng, n - (shape == "insert"), alpha)
    if shape == "insert":
        s.insert(rng.randint(0, len(s)), rng.choice(alpha))
    elif shape == "two":
        for _ in range(2):
            s.insert(rng.randint(0, len(s)), rng.choice(alpha))
        s = s[:n]
    elif shape == "change":
        i = rng.randrange(n)
        s[i] = rng.choice([c for c in alpha if c != s[i]] or alpha)
    return "".join(s)
def small(rng):
    return {"s": make(rng, rng.randint(1, 12), "abc"[:rng.randint(1, 3)], rng.choice(["pal", "insert", "insert", "two", "change", "random"]))}
def build(rng, n, k=26, shape="insert"):
    return {"s": make(rng, n, string.ascii_lowercase[:k], shape)}
