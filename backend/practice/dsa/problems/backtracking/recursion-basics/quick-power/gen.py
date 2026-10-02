def build(rng, bexp=18, eexp=18, mexp=9):
    return {"base": rng.randint(0, 10**bexp), "exp": rng.randint(0, 10**eexp), "mod": rng.randint(1, 10**mexp)}


def small(rng):
    return {"base": rng.randint(0, 20), "exp": rng.randint(0, 30), "mod": rng.randint(1, 50)}
