def validate(n, k):
    assert type(n) is int and 1 <= n <= 60, "1 <= n <= 60"
    assert type(k) is int and 1 <= k <= 2 ** (n - 1), "1 <= k <= 2^(n-1)"
