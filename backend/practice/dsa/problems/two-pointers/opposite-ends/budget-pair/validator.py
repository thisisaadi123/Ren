from ren_check import ints, integer
def validate(prices, budget):
    ints("prices", prices, 2, 100_000, -10**9, 10**9)
    assert all(prices[i] <= prices[i + 1] for i in range(len(prices) - 1)), "prices must be sorted"
    integer("budget", budget, -2 * 10**9, 2 * 10**9)
    seen, count = {}, 0
    for x in prices:
        count += seen.get(budget - x, 0)
        seen[x] = seen.get(x, 0) + 1
    assert count == 1, "exactly one pair must add up to budget"
