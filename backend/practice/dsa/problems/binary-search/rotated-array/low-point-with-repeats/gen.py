from ren_gen import ints
def make(rng, n, spread, shape):
    if shape == "plateau":
        a = [1] * n
        a[rng.randrange(n)] = 0
        i = a.index(0)
        return {"readings": a[i:] + a[:i] if rng.random() < 0.5 else a[i + 1:] + a[: i + 1]}
    a = sorted(ints(rng, n, -spread, spread))
    k = rng.randrange(n)
    return {"readings": a[k:] + a[:k]}
def small(rng):
    return make(rng, rng.randint(1, 8), rng.choice([1, 2, 5]), rng.choice(["plateau", "random"]))
def build(rng, n, spread=5000, shape="random"):
    return make(rng, n, spread, shape)
