from ren_gen import distinct


def build(rng, n, span=1_000_000_000):
    return {"codes": sorted(distinct(rng, n, -span, span))}


def small(rng):
    return build(rng, rng.randint(1, 9), rng.choice((10, 1000)))
