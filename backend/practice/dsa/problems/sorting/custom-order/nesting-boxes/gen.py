def small(rng):
    return {"boxes": [[rng.randint(1, 5), rng.randint(1, 5)] for _ in range(rng.randint(1, 7))]}
def build(rng, n, hi=10**5, shape="random"):
    if shape == "chain":
        return {"boxes": [[i + 1, i + 1] for i in range(n)][::-1]}
    if shape == "same-width":
        return {"boxes": [[7, rng.randint(1, hi)] for _ in range(n)]}
    return {"boxes": [[rng.randint(1, hi), rng.randint(1, hi)] for _ in range(n)]}
