def validate(a, b, k):
    for name, xs in (("a", a), ("b", b)):
        assert isinstance(xs, list) and 1 <= len(xs) <= 10**5, f"1 <= {name}.length <= 10^5"
        assert all(type(v) is int and -10**9 <= v <= 10**9 for v in xs), f"-10^9 <= {name}[i] <= 10^9"
        assert all(xs[i] <= xs[i + 1] for i in range(len(xs) - 1)), f"{name} is sorted"
    assert type(k) is int and 1 <= k <= min(len(a) * len(b), 10**4), "1 <= k <= min(|a||b|, 10^4)"
