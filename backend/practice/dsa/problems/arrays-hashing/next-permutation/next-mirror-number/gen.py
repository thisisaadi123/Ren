from ren_gen import word


def mirror(rng, n, alpha, half=None):
    if half is None:
        half = word(rng, n // 2, alpha)
    if half and half[0] == "0":
        half = rng.choice("123456789") + half[1:]
    mid = ""
    if n % 2:
        mid = rng.choice(alpha)
        if not half and mid == "0":
            mid = rng.choice("123456789")
    return half + mid + half[::-1]


def small(rng):
    alpha = "0123" if rng.random() < 0.6 else "0123456789"
    return {"code": mirror(rng, rng.randint(1, 8), alpha)}


def build(rng, n, shape="random", alpha="full"):
    digits = "0123456789" if alpha == "full" else "129"
    h = n // 2
    half = word(rng, h, digits)
    if shape == "descending":
        half = "".join(sorted(half, reverse=True))
    elif shape == "deep":
        half = "1" + "".join(sorted(word(rng, h - 1, "23456789"), reverse=True))
    elif shape == "tail":
        k = min(h, rng.randint(2, 60))
        half = half[:h - k] + "".join(sorted(half[h - k:], reverse=True))
    elif shape == "equal":
        half = rng.choice("123456789") * h
    return {"code": mirror(rng, n, digits, half)}
