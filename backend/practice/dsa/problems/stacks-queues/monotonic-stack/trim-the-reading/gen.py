def digits(rng, n, alpha="0123456789"):
    s = rng.choice("123456789") + "".join(rng.choice(alpha) for _ in range(n - 1))
    return s
def small(rng):
    n = rng.randint(1, 10)
    num = "0" if n == 1 and rng.random() < 0.1 else digits(rng, n, rng.choice(["0123456789", "019", "12"]))
    return {"num": num, "k": rng.randint(1, len(num))}
def build(rng, n, k, shape="random"):
    k = min(int(k), n)
    if shape == "rising":
        num = "".join(str(min(9, 1 + 9 * i // n)) for i in range(n))
    elif shape == "falling":
        num = "".join(str(9 - min(8, 9 * i // n)) for i in range(n))
    elif shape == "zeros":
        num = "1" + "".join(rng.choice("0000001") for _ in range(n - 1))
    elif shape == "same":
        num = "7" * n
    else:
        num = digits(rng, n)
    return {"num": num, "k": k}
