import string
AL = string.ascii_letters + string.digits + ".,"
def small(rng):
    n = rng.randint(1, 20)
    return {"text": "".join(rng.choice(AL) for _ in range(n)), "rows": rng.randint(1, min(8, n + 2))}
def build(rng, n, rows):
    return {"text": "".join(rng.choice(AL) for _ in range(n)), "rows": rows}
