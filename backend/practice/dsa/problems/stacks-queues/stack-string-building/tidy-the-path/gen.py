def build(rng, n, shape="random"):
    names = ["a", "b", "home", "x_1", "...", "..a", ".b", "lib"]
    parts, size = [], 0
    while size < n:
        r = rng.random()
        if shape == "up":
            piece = ".." if r < 0.6 else rng.choice(names)
        elif shape == "deep":
            piece = rng.choice(names) if r < 0.9 else ".."
        else:
            piece = ".." if r < 0.25 else "." if r < 0.35 else "" if r < 0.45 else rng.choice(names)
        parts.append(piece)
        size += len(piece) + 1
    path = "/" + "/".join(parts)
    if rng.random() < 0.3:
        path += "/"
    return {"path": path[:n] if len(path) > n and path[n - 1] != "/" else path[:n] or "/"}


def small(rng):
    return build(rng, rng.randint(1, 14), rng.choice(("random", "up", "deep")))
