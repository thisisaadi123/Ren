from ren_gen import word
def make(rng, n, alpha, wlen, tlen, shape):
    words = []
    for _ in range(n):
        words.append(word(rng, rng.randint(1, wlen), alpha))
    if shape == "fitall":
        tiles = "".join(words)[:100]
        extra = 100 - len(tiles)
        tiles += word(rng, rng.randint(0, max(0, min(extra, 10))), alpha)
    else:
        tiles = word(rng, tlen, alpha)
    points = [rng.randint(0, 10) for _ in range(26)]
    if shape == "flat":
        points = [1] * 26
    return {"words": words, "tiles": tiles or alpha[0], "points": points}
def small(rng):
    alpha = "abcdefghij"[:rng.randint(2, 5)]
    return make(rng, rng.randint(1, 4), alpha, 3, rng.randint(1, 8), "random")
def build(rng, n, alpha=5, wlen=6, tlen=30, shape="random"):
    return make(rng, n, "abcdefghijklmnopqrstuvwxyz"[:alpha], wlen, tlen, shape)
