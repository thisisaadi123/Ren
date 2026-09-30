import string
def make(rng, n, letters):
    while True:
        g = "".join(sorted(rng.choice(letters) for _ in range(n)))
        if len(set(g)) >= 2:
            return {"gates": g, "current": rng.choice(string.ascii_lowercase)}
def small(rng):
    return make(rng, rng.randint(2, 6), "acegx")
def build(rng, n, letters="abcdefghijklmnopqrstuvwxyz"):
    return make(rng, n, letters)
