from ren_gen import ints
def small(rng):
    return {"cells": ints(rng, rng.randint(1, 8), 0, 3), "blank": rng.randint(0, 3)}
def build(rng, n, hi=100, blank=0):
    return {"cells": ints(rng, n, 0, hi), "blank": blank}
