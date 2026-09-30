from ren_gen import ints
def small(rng):
    return {"nums": ints(rng, rng.randint(1, 8), 0, 20)}
def build(rng, n, hi=10**9, shape="random"):
    if shape == "clustered":
        a = ints(rng, n // 2, 0, 1000) + ints(rng, n - n // 2, hi - 1000, hi)
    elif shape == "even":
        step = hi // n
        a = [i * step for i in range(n)]
        a[rng.randrange(n)] += step // 2
    else:
        a = ints(rng, n, 0, hi)
    rng.shuffle(a)
    return {"nums": a}
