def small(rng):
    return {"text": "".join(rng.choice("ab-1 Z") for _ in range(rng.randint(1, 8)))}
def build(rng, n, alphabet="abcdefXYZ-_ 0123!"):
    return {"text": "".join(rng.choice(alphabet) for _ in range(n))}
