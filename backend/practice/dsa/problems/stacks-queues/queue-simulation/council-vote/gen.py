def build(rng, n, larks=50, shape="random"):
    if shape == "blocks":
        k = n * larks // 100
        return {"council": "L" * k + "O" * (n - k)}
    if shape == "alternate":
        return {"council": "".join("LO"[i % 2] for i in range(n))}
    return {"council": "".join("L" if rng.random() < larks / 100 else "O" for _ in range(n))}


def small(rng):
    return build(rng, rng.randint(1, 9), rng.choice((30, 50, 70)), rng.choice(("random", "random", "blocks")))
