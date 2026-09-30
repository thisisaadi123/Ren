def small(rng):
    return build(rng, rng.randint(1, 7), "abc")
def build(rng, n, alphabet="abcdefghijklmnopqrstuvwxyz", shape="random"):
    half = [rng.choice(alphabet) for _ in range(n // 2)]
    mid = [rng.choice(alphabet)] if n % 2 else []
    letters = half + half + mid
    if shape == "reversed-halves":
        half.sort()
        letters = half + mid + half
    else:
        rng.shuffle(letters)
    return {"word": "".join(letters)}
