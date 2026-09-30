from ren_gen import word
def small(rng):
    u = word(rng, rng.randint(1, 4), "ab")
    s = u * rng.randint(1, 4)
    if rng.random() < 0.3:
        s = s + rng.choice("ab")
    return {"s": s[:12]}
def build(rng, n, unit=1, alpha="ab", broken=False):
    u = word(rng, unit, alpha)
    s = u * max(1, n // unit)
    if broken not in (False, "false"):
        s = list(s)
        i = rng.randrange(len(s))
        s[i] = "z"
        s = "".join(s)
    return {"s": s}
