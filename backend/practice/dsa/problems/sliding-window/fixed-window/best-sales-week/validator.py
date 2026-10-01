def validate(sales, k):
    assert isinstance(sales, list) and 1 <= len(sales) <= 100_000, "1 <= sales.length <= 10^5"
    assert all(type(v) is int and -10**4 <= v <= 10**4 for v in sales), "-10^4 <= sales[i] <= 10^4"
    assert type(k) is int and 1 <= k <= len(sales), "1 <= k <= sales.length"
