def validate(prices):
    assert isinstance(prices, list) and 1 <= len(prices) <= 100_000, "1 <= prices.length <= 10^5"
    assert all(type(v) is int and 1 <= v <= 30_000 for v in prices), "1 <= prices[i] <= 3 * 10^4"
