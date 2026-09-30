def small(rng):
    n = rng.randint(1, 5)
    return {"toppings": rng.sample(range(-10, 11), n)}
def build(rng, n, shape="random"):
    t = rng.sample(range(-10, 11), n)
    if shape == "desc":
        t.sort(reverse=True)
    return {"toppings": t}
