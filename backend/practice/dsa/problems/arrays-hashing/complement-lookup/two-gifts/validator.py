from ren_check import ints, integer
import collections
def validate(prices, budget):
    ints("prices", prices, 2, 100_000, -10**9, 10**9)
    integer("budget", budget, -2 * 10**9, 2 * 10**9)
    count = collections.Counter(prices)
    pairs = 0
    for x, c in count.items():
        y = budget - x
        if x < y:
            pairs += c * count.get(y, 0)
        elif x == y:
            pairs += c * (c - 1) // 2
    assert pairs == 1, "exactly one pair must add up to budget (found %d)" % pairs
