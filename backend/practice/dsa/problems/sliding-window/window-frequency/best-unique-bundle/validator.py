def validate(prices, k):
    assert isinstance(prices, list) and 1 <= len(prices) <= 100_000, "1 <= prices.length <= 10^5"
    assert all(type(v) is int and 1 <= v <= 10**5 for v in prices), "1 <= prices[i] <= 10^5"
    assert type(k) is int and 1 <= k <= len(prices), "1 <= k <= prices.length"
