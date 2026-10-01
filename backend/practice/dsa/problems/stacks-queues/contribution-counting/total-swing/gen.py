from ren_gen import ints


def build(rng, n, hi=10**6, shape="random"):
    a = ints(rng, n, -hi, hi)
    if shape == "ascending":
        a.sort()
    elif shape == "zigzag":
        a = [hi if i % 2 else -hi for i in range(n)]
    elif shape == "equal":
        a = [rng.randint(-hi, hi)] * n
    return {"readings": a}


def small(rng):
    return build(rng, rng.randint(1, 8), rng.choice((2, 10)), rng.choice(("random", "random", "equal")))
