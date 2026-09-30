def small(rng):
    n = rng.randint(1, 12)
    return {"s": "".join(rng.choice("()()ab") for _ in range(n))}
def build(rng, n, shape="random"):
    if shape == "opens":
        s = "".join(rng.choice("((((a") for _ in range(n))
    elif shape == "closes":
        s = "".join(rng.choice("))))b") for _ in range(n))
    elif shape == "letters":
        s = "".join(rng.choice("abcdefgh") for _ in range(n))
    elif shape == "open-tail":
        h = n // 2
        s = "".join(rng.choice("()xy") for _ in range(h)) + "(" * (n - h)
    else:
        s = "".join(rng.choice("()()abc") for _ in range(n))
    return {"s": s}
