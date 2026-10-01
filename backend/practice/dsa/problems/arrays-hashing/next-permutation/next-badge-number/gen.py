from ren_gen import word


def fix(s):
    return s if s[0] != "0" else "1" + s[1:]


def small(rng):
    alpha = "0123" if rng.random() < 0.6 else "0123456789"
    return {"code": fix(word(rng, rng.randint(1, 7), alpha))}


def build(rng, n, shape="random", alpha="full"):
    digits = "0123456789" if alpha == "full" else "129"
    s = list(word(rng, n, digits))
    if shape == "descending":
        s.sort(reverse=True)
    elif shape == "equal":
        s = [rng.choice("123456789")] * n
    elif shape == "deep":
        rest = sorted(word(rng, n - 1, "23456789"), reverse=True)
        s = ["1"] + rest
    elif shape == "tail":
        k = min(n, rng.randint(2, 60))
        s[n - k:] = sorted(s[n - k:], reverse=True)
    return {"code": fix("".join(s))}
