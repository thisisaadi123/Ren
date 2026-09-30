import string
CH = string.ascii_lowercase
PUNCT = string.ascii_letters + string.digits + ".,!?'-"
def w(rng, k, alpha=CH):
    return "".join(rng.choice(alpha) for _ in range(k))
def small(rng):
    width = rng.randint(3, 9)
    words = [w(rng, rng.randint(1, min(4, width)), "abc") for _ in range(rng.randint(1, 6))]
    return {"words": words, "width": width}
def build(rng, n, width, maxlen=0, shape="random"):
    maxlen = min(maxlen or width, width)
    if shape == "ones":
        return {"words": [w(rng, 1) for _ in range(n)], "width": width}
    if shape == "full":
        return {"words": [w(rng, width) for _ in range(n)], "width": width}
    if shape == "exact":
        words = []
        while len(words) < n:
            left = width
            while left > 0 and len(words) < n:
                k = rng.randint(1, min(maxlen, left))
                words.append(w(rng, k))
                left -= k + 1
        return {"words": words, "width": width}
    if shape == "long-short":
        return {"words": [w(rng, maxlen if i % 2 else 1) for i in range(n)], "width": width}
    alpha = PUNCT if shape == "punct" else CH
    return {"words": [w(rng, rng.randint(1, maxlen), alpha) for _ in range(n)], "width": width}
