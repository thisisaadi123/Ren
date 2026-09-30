from ren_gen import ints
def small(rng):
    return {"roundTime": ints(rng, rng.randint(1, 4), 1, 6), "totalRounds": rng.randint(1, 15)}
def build(rng, n, hi=10**7, rounds=10**7):
    return {"roundTime": ints(rng, n, 1, hi), "totalRounds": rng.randint(max(1, rounds // 2), rounds)}
