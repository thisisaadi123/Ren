import collections
def make(rng, n, lo, hi):
    while True:
        prices = [rng.randint(lo, hi) for _ in range(n)]
        i, j = rng.sample(range(n), 2)
        budget = prices[i] + prices[j]
        count = collections.Counter(prices)
        pairs = sum(c * count.get(budget - x, 0) for x, c in count.items() if x < budget - x)
        pairs += sum(c * (c - 1) // 2 for x, c in count.items() if 2 * x == budget)
        if pairs == 1:
            return {"prices": prices, "budget": budget}
def small(rng):
    return make(rng, rng.randint(2, 7), -5, 10)
def build(rng, n, lo=-10**9, hi=10**9):
    return make(rng, n, lo, hi)
